class GenerationsController < ApplicationController
  skip_before_action :authenticate!, only: :health

  # GET /health
  def health
    render json: { status: "ok" }
  end

  # POST /generate
  # Expected params:
  #   character_id     — string, must exist in Characters registry
  #   scenario         — string, what the character is doing
  #   supporting       — string (optional), adults in the scene
  #   callback_url     — string, where to POST the result (omit for sync mode)
  #   sync             — boolean (optional), process inline and return image_url directly
  def create
    character_id = params[:character_id].to_s.strip
    scenario     = params[:scenario].to_s.strip
    supporting   = params[:supporting].to_s.strip
    callback_url = params[:callback_url].to_s.strip
    sync_mode    = params[:sync].in?(["true", true, "1", 1])

    return render json: { error: "Missing required field: character_id" }, status: :bad_request if character_id.blank?
    return render json: { error: "Missing required field: scenario" }, status: :bad_request if scenario.blank?
    return render json: { error: "Missing required field: callback_url" }, status: :bad_request if !sync_mode && callback_url.blank?

    unless Characters.exists?(character_id)
      return render json: { error: "Unknown character_id: '#{character_id}'" }, status: :bad_request
    end

    # Scrub PII before anything else
    scenario,   = PiiScrubber.scrub(scenario)
    supporting, = PiiScrubber.scrub(supporting)

    # Moderation check — reject early before incurring generation cost
    flagged = ModerationService.flagged_categories(scenario)
    if flagged.any?
      return render json: { error: "Scenario failed content moderation", categories: flagged },
                    status: :unprocessable_entity
    end

    if sync_mode
      result = GenerationJob.perform_now(character_id, scenario, supporting, nil)
      if result[:error]
        render json: { status: "error", message: result[:error] }, status: :internal_server_error
      else
        render json: { status: "success", image_url: result[:image_url] }
      end
    else
      GenerationJob.perform_later(character_id, scenario, supporting, callback_url)
      render json: { status: "accepted", message: "Image generation started" }, status: :accepted
    end
  end
end
