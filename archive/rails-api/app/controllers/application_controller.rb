class ApplicationController < ActionController::API
  before_action :authenticate!

  private

  def authenticate!
    token = request.headers["Authorization"]&.sub(/\ABearer\s+/, "")
    return if token == ENV.fetch("INBOUND_BEARER_TOKEN")

    render json: { error: "Unauthorized" }, status: :unauthorized
  end
end
