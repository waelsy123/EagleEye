class VideosController < ApplicationController
  before_action :set_video, only: [:show, :edit, :update, :destroy]

  # GET /videos
  # GET /videos.json
  def index
    @search = Video.search(params[:q])
    @videos = @search.result
    @search.build_condition if @search.conditions.empty?
    @search.build_sort if @search.sorts.empty?
  end

  # GET /videos/1
  # GET /videos/1.json
  def show
    video_attributes
  end

  # GET /videos/new
  def new
    @video = Video.new
    video_attributes
  end

  # GET /videos/1/edit
  def edit
    video_attributes
  end

  # POST /videos
  # POST /videos.json
  def create
    @video = Video.new(video_params)
    video_attributes

    respond_to do |format|
      if @video.save
        format.html { redirect_to @video, notice: 'Video was successfully created.' }
        format.json { render :show, status: :created, location: @video }
      else
        format.html { render :new }
        format.json { render json: @video.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /videos/1
  # PATCH/PUT /videos/1.json
  def update
    video_attributes
    respond_to do |format|
      if @video.update(video_params)
        format.html { redirect_to @video, notice: 'Video was successfully updated.' }
        format.json { render :show, status: :ok, location: @video }
      else
        format.html { render :edit }
        format.json { render json: @video.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /videos/1
  # DELETE /videos/1.json
  def destroy
    @video.destroy
    respond_to do |format|
      format.html { redirect_to videos_url, notice: 'Video was successfully destroyed.' }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_video
      @video = Video.find(params[:id])
    end

    # Never trust parameters from the scary internet, only allow the white list through.
    def video_params
      video_custom_params = params.require(:video).permit!.except(:id)
      if video_custom_params[:custom_tag].empty?
        video_custom_params.except(:custom_tag, :custom_value)
      else
        custom_param = ActionController::Parameters.new(
          { video_custom_params[:custom_tag].downcase.to_sym => video_custom_params[:custom_value] })
        video_custom_params.except(:custom_tag, :custom_value).merge(custom_param)
      end
    end

    def video_attributes
      keys_blacklist = %W(_id author_id updated_at created_at) #these are the fields to hide
      @video_attributes = @video.attributes.except(*keys_blacklist)
    end
end
