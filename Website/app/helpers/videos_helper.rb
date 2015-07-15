module VideosHelper
	def all_attributes
		keys_blacklist = %W(_id author_id updated_at created_at) #these are the fields to hide
		attributes = Hash.new
		Video.each do |video|
			attributes.merge!(video.attributes)
		end
		attributes.except(*keys_blacklist).keys
	end
end
