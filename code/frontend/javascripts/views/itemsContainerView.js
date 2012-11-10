var ItemsContainerView = Backbone.View.extend({
	el: $("#itemsContainer"),

	initialize: function(){
		this.model = new Track(window.trackData);
		
		self = this;
		this.model.items.on("add", function(model){
			var itemView = new ItemView({model:model});
			$(self.el).append($(itemView.el).html());
		});

		this.render();
	},

	render: function(){
		return this;
	}
});