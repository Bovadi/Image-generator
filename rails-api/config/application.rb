require_relative "boot"
require "rails"
require "action_controller/railtie"
require "action_dispatch/railtie"
require "active_job/railtie"

Bundler.require(*Rails.groups)

module BipImageGenerator
  class Application < Rails::Application
    config.load_defaults 7.1
    config.api_only = true

    # Use async adapter for background jobs (swap to Sidekiq in production)
    config.active_job.queue_adapter = :async

    config.autoload_lib(ignore: %w[assets tasks])
  end
end
