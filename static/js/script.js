
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
                if (response.status === 'success') {
                    $('#content-1').prepend('<div class="alert alert-success" role="alert">'+response.message+'</div>')
                    $('#list-group').append('<div class="list-group-item list-group-item-action active py-3 lh-sm" aria-current="true"><div class="d-flex w-100 align-items-center justify-content-between"><a href="view-list/'+response.todo_id+'" class="item-name"><strong class="mb-1">'+response.name+'</strong></a><span class="badge bg-dark-subtle border border-dark-subtle text-dark-emphasis rounded-pill" style="color: rgb(54, 53, 53);">'+response.item_num+'</span><a href="edit-list/'+response.todo_id+'" class="item-name"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-fill" viewBox="0 0 16 16"><path d="M12.854.146a.5.5 0 0 0-.707 0L10.5 1.793 14.207 5.5l1.647-1.646a.5.5 0 0 0 0-.708zm.646 6.061L9.793 2.5 3.293 9H3.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.207zm-7.468 7.468A.5.5 0 0 1 6 13.5V13h-.5a.5.5 0 0 1-.5-.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.5-.5V10h-.5a.5.5 0 0 1-.175-.032l-.179.178a.5.5 0 0 0-.11.168l-2 5a.5.5 0 0 0 .65.65l5-2a.5.5 0 0 0 .168-.11z"/></svg></a><a href="del_list/'+response.todo_id+'" class="item-name"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3-fill" viewBox="0 0 16 16"><path d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06m6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528M8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"/></svg></a></div></div>');
                }
            },
            error: function(error) {
                let errorMessage = response.responseJSON.message || "An error occurred.";
                 $('#content-1').prepend('<div class="alert alert-danger" role="alert">'+errorMessage+'</div>')
            }
       });

    });
});