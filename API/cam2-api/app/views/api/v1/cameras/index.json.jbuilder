json.cameras(@cameras) do |camera|
	json.url camera.url
	json.city camera.state
	json.state camera.state
end
