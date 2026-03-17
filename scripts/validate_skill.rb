#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"
require "pathname"

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_PROPERTIES = ["name", "description", "license", "allowed-tools", "metadata"].freeze

def validate_skill(skill_path)
  skill_dir = Pathname.new(skill_path)
  skill_md = skill_dir.join("SKILL.md")
  return [false, "SKILL.md not found"] unless skill_md.exist?

  content = skill_md.read
  return [false, "No YAML frontmatter found"] unless content.start_with?("---")

  match = content.match(/\A---\n(.*?)\n---/m)
  return [false, "Invalid frontmatter format"] unless match

  frontmatter_text = match[1]

  begin
    frontmatter = YAML.safe_load(frontmatter_text, permitted_classes: [], aliases: false)
  rescue Psych::SyntaxError => e
    return [false, "Invalid YAML in frontmatter: #{e.message}"]
  end

  return [false, "Frontmatter must be a YAML dictionary"] unless frontmatter.is_a?(Hash)

  unexpected_keys = frontmatter.keys.map(&:to_s) - ALLOWED_PROPERTIES
  unless unexpected_keys.empty?
    allowed = ALLOWED_PROPERTIES.sort.join(", ")
    unexpected = unexpected_keys.sort.join(", ")
    return [
      false,
      "Unexpected key(s) in SKILL.md frontmatter: #{unexpected}. Allowed properties are: #{allowed}"
    ]
  end

  return [false, "Missing 'name' in frontmatter"] unless frontmatter.key?("name")
  return [false, "Missing 'description' in frontmatter"] unless frontmatter.key?("description")

  name = frontmatter["name"]
  return [false, "Name must be a string, got #{name.class}"] unless name.is_a?(String)

  trimmed_name = name.strip
  unless trimmed_name.empty?
    unless /\A[a-z0-9-]+\z/.match?(trimmed_name)
      return [
        false,
        "Name '#{trimmed_name}' should be hyphen-case (lowercase letters, digits, and hyphens only)"
      ]
    end

    if trimmed_name.start_with?("-") || trimmed_name.end_with?("-") || trimmed_name.include?("--")
      return [
        false,
        "Name '#{trimmed_name}' cannot start/end with hyphen or contain consecutive hyphens"
      ]
    end

    if trimmed_name.length > MAX_SKILL_NAME_LENGTH
      return [
        false,
        "Name is too long (#{trimmed_name.length} characters). Maximum is #{MAX_SKILL_NAME_LENGTH} characters."
      ]
    end
  end

  description = frontmatter["description"]
  return [false, "Description must be a string, got #{description.class}"] unless description.is_a?(String)

  trimmed_description = description.strip
  unless trimmed_description.empty?
    return [false, "Description cannot contain angle brackets (< or >)"] if trimmed_description.include?("<") || trimmed_description.include?(">")

    if trimmed_description.length > 1024
      return [
        false,
        "Description is too long (#{trimmed_description.length} characters). Maximum is 1024 characters."
      ]
    end
  end

  [true, "Skill is valid!"]
end

if ARGV.length != 1
  warn "Usage: ruby scripts/validate_skill.rb <skill_directory>"
  exit 1
end

valid, message = validate_skill(ARGV[0])
puts message
exit(valid ? 0 : 1)
