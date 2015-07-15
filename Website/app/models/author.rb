class Author
  include Mongoid::Document
  include Mongoid::Attributes::Dynamic
  include Mongoid::Timestamps

  field :id, as: :username, type: String

  validates_presence_of :username
  has_many :videos, dependent: :delete

  def self.ransackable_attributes(auth_object = nil)
    AuthorsController.helpers.all_attributes
  end
end
