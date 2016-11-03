class AddFieldsToCameras < ActiveRecord::Migration[5.0]
  def change
	add_column :cameras, :camera_type, :string
	add_column :cameras, :source, :string
	add_column :cameras, :camera_key, :string
	add_column :cameras, :latitude, :float
	add_column :cameras, :longitude, :float
	add_column :cameras, :resolution_width, :integer
	add_column :cameras, :resolution_height, :integer
	add_column :cameras, :frame_rate, :float
	add_column :cameras, :active, :bool
	add_column :cameras, :time_zone, :string
	add_column :cameras, :inactive_since, :datetime
	add_column :cameras, :indoors, :boolean
  end
end
