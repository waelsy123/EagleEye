class Video
  include Mongoid::Document
  include Mongoid::Attributes::Dynamic
  include Mongoid::Timestamps
  
  field :id, as: :title, type: String

  validates_presence_of :author_id, :title
  belongs_to :author

  def self.ransackable_attributes(auth_object = nil)
    VideosController.helpers.all_attributes
  end
end
