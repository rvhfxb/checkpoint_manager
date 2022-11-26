function load_checkpoint(button, title){
    textarea = gradioApp().querySelector('#ckectpoint_to_load textarea')
    textarea.value = title
	textarea.dispatchEvent(new Event("input", { bubbles: true }))
    gradioApp().querySelector('#load_checkpoint_button').click()
}
    

function save_json(_, _){
    arr = []
    gradioApp().querySelectorAll('#tab_checkpoint_manager .checkpoint_manager_row').forEach(function(row){
        arr.push({
            "title": row.dataset.title,
            "hash": row.querySelector('.checkpoint_manager_hash').innerHTML,
            "comment": row.querySelector('.checkpoint_manager_comment').value,
            "top": row.querySelector('.checkpoint_manager_top').checked,
        })
    })

    return [JSON.stringify(arr)]
}

function set_y_values(_, _){
    selected = []
    gradioApp().querySelectorAll('#tab_checkpoint_manager .checkpoint_manager_select').forEach(function(x){
        if(x.checked){
            selected.push(x.closest(".checkpoint_manager_row").dataset.title)
        }
    })

    gradioApp().querySelector('#y_type').nextElementSibling.querySelector("textarea").value = selected.join(",");
}