//add another row to the ingredients for the recipes
function add_row()
{
    //get the total number of forms
    var formCount = $('.form_row').length;

    //clone the first form row that we find
    var $form_row_clone = $(".form_row").first().clone();

    //set the selected option of the select box to null
    $form_row_clone.find("select").val("");
    //clear the input text
    $form_row_clone.find("input").val("");
    //unhide all of the hidden options for selectors
    $form_row_clone.find("select").find("option").show();

    //get all of the input fields in the new row
    var $input_fields = $form_row_clone.find("input,select");

    //for each of the input fields change the row number in id and name
    $input_fields.each(function(){
       $(this).attr("id", $(this).attr("id").replace(0,formCount));
       $(this).attr("name", $(this).attr("name").replace(0,formCount));
    });

    $form_row_clone.find("[id$='id']").removeAttr('value');

    //increment the number of forms 
    $('[id$=TOTAL_FORMS]').val(formCount + 1);
    //add the cloned table row to the table
    $(".form_row_table").append($form_row_clone);
    //bind get_valid_units on change to update units on ingredient change
    $form_row_clone.change(get_valid_units);
    
}

//remove a row from the ingredients
function remove_row()
{
    //get the total number of forms
    var formCount = $('.form_row').length;

    //only remove rows when there is more than one left
    if(formCount > 1)
    {
        //remove the last form from the document
        var $form_row = $(".form_row").last();
        $form_row.remove();
        
        //decrement the number of forms 
        $('#id_recipeingredient_set-TOTAL_FORMS').val(formCount - 1);
    }
}

//retreive the key of select field passed in and return a list
//of valid keys for units that can be used with the specified unit
function get_valid_units(){

   var ingredient_id = $(this).find('option:selected').attr('value');
   var unit = $(this).find("[name$=unit]");
   //when no ingredient is selected the selector returns ""
   //change this to 0 to be more consistant in python side of app
   if (ingredient_id == ""){
        ingredient_id = 0
   }
   
   $.getJSON("/measures/ajax/getunit",{ingredient : ingredient_id},
             function(result){
                //for each of the children in the unit selector 
                $.each(unit.children(), function(index,child){
                    var value = $(child).attr("value");
                    //if the value is in the list
                    if (jQuery.inArray(value, result) != -1){
                        //show the child
                        $(child).show();
                    }else{
                        //hide the child
                        $(child).hide();
                    
                    }
                });
             });
}

