class AddCountryToCameras < ActiveRecord::Migration[5.0]
  def change
    add_column :cameras, :country, :string
  end
end
