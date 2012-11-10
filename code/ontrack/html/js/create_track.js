 console.log("niads");
 
 $(document).ready(function() {
     $('#title').editable({submit:"save"});
     
     $('#description').editable({submit:"save", type:"textarea"});
 });