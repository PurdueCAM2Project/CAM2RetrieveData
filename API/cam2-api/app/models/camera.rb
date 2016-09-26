class Camera < ApplicationRecord
	validates :name, presence: true
	validates :city, presence: true
	validates :state, presence: true
	validates :url, presence: true, uniqueness: true
	validates :country, presence: true
end
