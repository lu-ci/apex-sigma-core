#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"
require "childprocess"

INFO = YAML.load_file("info/version.yml").freeze
CODENAME = INFO["codename"].downcase
VERSION = INFO["version"]
REGISTRY = "git.luciascipher.com"
NAMESPACE = "lucia"
IMAGE = "apex-sigma"

def tagged(tag)
  "#{REGISTRY}/#{NAMESPACE}/#{IMAGE}:#{tag}"
end

@tags = [
  tagged(CODENAME),
  tagged("#{VERSION['major']}.#{VERSION['minor']}.#{VERSION['patch']}"),
  tagged("#{VERSION['major']}.#{VERSION['minor']}"),
  tagged(VERSION['major']),
  tagged("latest")
].freeze

def build
  tags = @tags.flat_map { |t| ["--tag", t] }
  cmd = ["docker", "build"] + tags << "."
  ChildProcess.build(*cmd).tap do |p|
    p.io.stdout = $stdout
    p.io.stderr = $stderr
    p.start
    p.wait
  end
end

def push
  @tags.each do |tag|
    ChildProcess.build("docker", "push", tag).tap do |p|
      p.io.stdout = $stdout
      p.io.stderr = $stderr
      p.start
      p.wait
    end
  end
end

def show
  puts @tags
end

case ARGV.first
when "build" then build
when "push" then push
when "show" then show
end
