class AuthorsController < ApplicationController
  before_action :set_author, only: [:show, :edit, :update, :destroy]

  # GET /authors
  # GET /authors.json
  def index
    @search = Author.search(params[:q])
    @authors = @search.result
    @search.build_condition if @search.conditions.empty?
    @search.build_sort if @search.sorts.empty?
  end

  # GET /authors/1
  # GET /authors/1.json
  def show
    author_attributes
  end

  # GET /authors/new
  def new
    @author = Author.new
    author_attributes
  end

  # GET /authors/1/edit
  def edit
    author_attributes
  end

  # POST /authors
  # POST /authors.json
  def create
    @author = Author.new(author_params)
    author_attributes

    respond_to do |format|
      if @author.save
        format.html { redirect_to @author, notice: 'Author was successfully created.' }
        format.json { render :show, status: :created, location: @author }
      else
        format.html { render :new }
        format.json { render json: @author.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /authors/1
  # PATCH/PUT /authors/1.json
  def update
    author_attributes
    respond_to do |format|
      if @author.update(author_params)
        format.html { redirect_to @author, notice: 'Author was successfully updated.' }
        format.json { render :show, status: :ok, location: @author }
      else
        format.html { render :edit }
        format.json { render json: @author.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /authors/1
  # DELETE /authors/1.json
  def destroy
    @author.destroy
    respond_to do |format|
      format.html { redirect_to authors_url, notice: 'Author was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_author
      @author = Author.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def author_params
      author_custom_params = params.require(:author).permit!.except(:id)
      if author_custom_params[:custom_tag].empty?
        author_custom_params.except(:custom_tag, :custom_value)
      else
        custom_param = ActionController::Parameters.new(
          { author_custom_params[:custom_tag].downcase.to_sym => author_custom_params[:custom_value] })
        author_custom_params.except(:custom_tag, :custom_value).merge(custom_param)
      end
    end
    
    def author_attributes
      keys_blacklist = %W(_id updated_at created_at) #these are the fields to hide
      @author_attributes = @author.attributes.except(*keys_blacklist)
    end
end
