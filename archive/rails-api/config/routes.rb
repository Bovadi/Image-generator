Rails.application.routes.draw do
  post "/generate", to: "generations#create"
  get  "/health",   to: "generations#health"
end
