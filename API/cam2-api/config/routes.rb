require 'api_constraint.rb'
Rails.application.routes.draw do
	scope module: :v1, constraints: ApiConstraint.new(version: 1) do
		resources :cameras
	end
end
