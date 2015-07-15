module Ransack
  module Adapters
    module Mongoid
      class Context < ::Ransack::Context
        def type_for(attr)
          return nil unless attr && attr.valid?
          name    = attr.arel_attribute.name.to_s
          # table   = attr.arel_attribute.relation.table_name

          # schema_cache = @engine.connection.schema_cache
          # raise "No table named #{table} exists" unless schema_cache.table_exists?(table)
          # schema_cache.columns_hash(table)[name].type

          # when :date
          # when :datetime, :timestamp, :time
          # when :boolean
          # when :integer
          # when :float
          # when :decimal
          # else # :string

          name = '_id' if name == 'id'

          #t = object.klass.fields[name].type
          t = :string

          t.to_s.demodulize.underscore.to_sym
        end
      end
    end
  end
end
