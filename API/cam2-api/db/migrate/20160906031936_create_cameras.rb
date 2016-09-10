class CreateCameras < ActiveRecord::Migration[5.0]
  def change
    create_table :cameras do |t|
      t.string :name
      t.string :city
      t.string :state
      t.string :url

      t.timestamps
    end
  end
end
