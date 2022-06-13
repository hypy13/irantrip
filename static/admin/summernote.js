function init_ckEditors() {
    $('.summernote').each(function (_, elem) {
        if (!$(this).parents('.empty-form').length) {
            if (!CKEDITOR.instances[elem.id]) {
                CKEDITOR.replace(elem.id);
            }
        }
    })

    $('.summernote-inline').each(function (elem) {
        CKEDITOR.inline(this.name);
    })
}

$(document).ready(function () {
    // CKEDITOR.disableAutoInline = true;
    init_ckEditors()
})

$(document).on("click", ".add-row a", function () {
    init_ckEditors()
})