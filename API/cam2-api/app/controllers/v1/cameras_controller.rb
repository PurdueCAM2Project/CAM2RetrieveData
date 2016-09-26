module V1
	class CamerasController < ApplicationController
		include ActionController::HttpAuthentication::Token::ControllerMethods
		before_action :restrict_access
	
		def create
			@camera = Camera.create(camera_params)
			if @camera.save
				render json: {
					status: 200,
					message: "Successfully created camera",
					camera: @camera
				}.to_json
			else
				render json: @camera.errors, status: :unprocessable_entity
			end
		end

		def index
			@cameras = Camera.all
		end

		private
			def restrict_access
				authenticate_or_request_with_http_token do |token, options|
					ApiKey.exists?(access_token: token)
				end
			end
		
			def camera_params
				params.require(:camera).permit(:name,:city,:state,:url,:country)
			end
	end
end
