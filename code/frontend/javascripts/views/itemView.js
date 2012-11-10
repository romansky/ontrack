var ItemView = Backbone.View.extend({
	tagName: "div",
	template: _.template($("#itemTemplate").html()),

	events: {
		"click .item" : "showItem",
	},

	initialize: function(){
		_.bindAll(this, "showItem");
		this.render();
	},

	render: function(){
		$(this.el).html(this.template(this.model.toJSON()));
		return this;
	},

	showItem: function(){
		//$("#iframeItem").src = this.model.get('url');
	}
});