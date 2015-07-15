module AuthorsHelper
	def all_attributes
        keys_blacklist = %W(_id updated_at created_at) #these are the fields to hide
		attributes = Hash.new
		Author.each do |author|
			attributes.merge!(author.attributes)
		end
		attributes.except(*keys_blacklist).keys
	end
end
