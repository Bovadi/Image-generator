require "open-uri"
require "securerandom"

class S3Service
  EXPIRY_DAYS = 14

  def self.upload_from_url(image_url)
    content    = URI.open(image_url).read
    key        = "images/#{SecureRandom.uuid}.png"
    bucket     = ENV.fetch("AWS_BUCKET_NAME")
    expires_at = Time.now + EXPIRY_DAYS * 24 * 60 * 60

    client.put_object(
      bucket:       bucket,
      key:          key,
      body:         content,
      content_type: "image/png",
      expires:      expires_at
    )

    client.presigned_url(
      :get_object,
      bucket:     bucket,
      key:        key,
      expires_in: EXPIRY_DAYS * 24 * 60 * 60
    )
  end

  private

  def self.client
    @client ||= Aws::S3::Client.new(
      region:            ENV.fetch("AWS_REGION", "us-east-1"),
      access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
      secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"]
    )
  end
end
