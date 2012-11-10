var Track = Backbone.Model.extend({
	url: function(){
		return "track.php";
	},
	defaults : {
		id: null,
		title: null,
		description: null,
		tags: null,
		level: null
	},

	items : null, // collection

	initialize: function(){
		this.items = new Items(null,{trackID: this.id});
		this.items.fetch({add: true});
	}
})