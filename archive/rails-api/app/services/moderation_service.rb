class ModerationService
  def self.flagged_categories(text)
    client   = OpenAI::Client.new(access_token: ENV.fetch("OPENAI_API_KEY"))
    response = client.moderations(parameters: { model: "omni-moderation-latest", input: text })
    result   = response.dig("results", 0)

    return [] unless result&.dig("flagged")

    result["categories"].select { |_category, flagged| flagged }.keys
  rescue => e
    Rails.logger.error("Moderation API error: #{e.message}")
    []
  end
end
