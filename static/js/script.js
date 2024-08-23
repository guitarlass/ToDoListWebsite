
$(document).ready(function() {
    $('#saveList').on('click', function(event) {
       let items = []
       $('.list-item').each(function() {
            name = $(this).find('.todo-label').text()
            isChecked = $(this).find('.todo-checkbox').is(':checked')? 1 : 0;

            items.push({item_name:name, checked:isChecked});
       });
       $.ajax({
            url: '/save_items',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(items),
            success: function(response) {
                alert('Items saved successfully!');
            },
            error: function(error) {
                console.error('Error saving items:', error);
            }
       });

    });
});