var Item = Backbone.Model.extend({
	url: function(){
	/* 
		return this.isNew() ? 
			"http://192.168.100.136/api/track/" + this.get("trackID") + "/items/"  + this.id:
			"http://192.168.100.136/api/track/" + this.get("trackID") + "/items";
	*/
	return "item.php";
	},

	defaults: {
		id: null,
		trackID: null,
		thumb: null,
		url: null,
	}

});