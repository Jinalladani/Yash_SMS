const BASE_URL = window.location.origin;

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(document).ready(() => {
    // $('.dateinput').datepicker({ format: "yyyy-mm-dd" });
    let element_date = $('.dateinput') 
    element_date.addClass("form-control")
    element_date.removeClass("dateinput")
    element_date.get(0).type = "date" 

    $(document).on('click', '.delete-record', function (event) {
        let url = this.href;
        let table = $(this).closest("table").DataTable();
        const csrftoken = getCookie('csrftoken');
        event.preventDefault();
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Yes, delete it!"
        }).then(function (result) {
            if (result.value) {
                $.ajax({
                    url: url,
                    method: "delete",
                    headers: {
                        'X-CSRFTOKEN': csrftoken
                    },
                    success: function (response) {
                        Swal.fire(
                            "Deleted!",
                            response.message,
                            "success"
                        ).then(function () {
                            table.ajax.reload();
                        });
                    },
                    error: function (error) {
                        Swal.fire(
                            "Not Deleted!",
                            "Something went wrong",
                            "error"
                        )
                    }
                });
            }
        });
    });    

    if (window.location.href.includes('upload-excel')) {


        let file_ids = [
            'uppy-income-category',
            'uppy-expense-category',
            'uppy-members-vendor-category',
            'uppy-members-category',
            'uppy-ledger-category'
        ]

        file_ids.forEach((id) => {

            try {
                let file_upload = Uppy.Core({
                    autoProceed: false,
                    restrictions: {
                        maxNumberOfFiles: 1,
                        minNumberOfFiles: 1,
                        allowedFileTypes: ['.xlsx']
                    }
                })
                    .use(Uppy.Dashboard, {
                        inline: true,
                        target: '#' + id,
                        height: 200,
                    })
                file_upload.use(Uppy.XHRUpload, {
                    endpoint: BASE_URL + '/api/accounting/upload-excel-api/',
                    headers: { 'X-CSRFTOKEN': getCookie('csrftoken') },
                    fieldName: id
                })
                file_upload.on('complete', (result) => {
                    console.log(result);
                })
            } catch (error) {
                console.log(error)
            }

        })
    }

    if(window.location.href.includes("income-expense-ledger")){
        $.ajax({
            url: "/api/accounting/get-category-header/",
            method: "GET",
            data: {type: "from-or-to-accounting"},
            success: (response) => {
                let from_or_to_account_select_html = "<select name='from_or_to_account' class='select form-control'></select>"
                $( "input[name=from_or_to_account]" ).replaceWith(from_or_to_account_select_html)
                $("select[name=from_or_to_account]").html("")
                $("select[name=from_or_to_account]").append("<option value=''>----------</option>")
                $("select[name=from_or_to_account]").append(
                    response.map((value, index) => (
                        `<option value='${value.name}'>${value.name}</option>`
                    ))   
                )
            },
            error: (error) => {
                console.log(error);
            }
        }) 


        $(document).on("change", "select[name=type]", (event) => {
            let type = $(event.target).val()
            let category_header_select_html = "<select name='category_header' class='select form-control'></select>"
            $.ajax({
                url: "/api/accounting/get-category-header/",
                method: "GET",
                data: {type},
                success: (response) => {
                    $( "input[name=category_header]" ).replaceWith(category_header_select_html)
                    $("select[name=category_header]").html("")
                    $("select[name=category_header]").append(
                        response.map((value, index) => (
                            `<option value='${value.category}'>${value.category}</option>`
                        ))   
                    )
                },
                error: (error) => {
                    console.log(error);
                }
            }) 
        });

    }
});

$(document).ready(() => {

    if (document.location.href.includes("income-category")) {
        var income_category_table = $('.table-income-category').dataTable({
            stateSave: true,
            select: {
                style: 'multi',
                selector: 'td:first-child .checkable',
            },
			dom: `<'row'<'col-sm-6 text-left'f><'col-sm-6 text-right'B>>
			<'row'<'col-sm-12'tr>>
			<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,

			buttons: [
                {
                    text: "Export to Excel",
                    action: () => {
                        window.location.href = '/accounting/export-income-category/';
                    }
                },
				{
                    text: 'Delete selected data',
                    action: function () {
                        Swal.fire({
                            title: "Are you sure?",
                            text: "You won't be able to revert this!",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonText: "Yes, delete it!"
                        }).then(function (result) {
                            if (result.value) {
                                const csrftoken = getCookie('csrftoken');
                                let pk_array = $.map(income_category_table.api().rows( { selected: true } ).data(), function (item) {
                                    return item[0];
                                });
                                $.ajax({
                                    url: '/api/accounting/bulk-delete/',
                                    method: "delete",
                                    data: {
                                        model_name: "IncomeCategoryModel",
                                        pk_array
                                    },        
                                    headers: {
                                        'X-CSRFTOKEN': csrftoken
                                    },
                                    success: function (response) {
                                        Swal.fire(
                                            "Deleted!",
                                            response.message,
                                            "success"
                                        ).then(function () {
                                            income_category_table.api().ajax.reload();
                                        });
                                    },
                                    error: function (error) {
                                        Swal.fire(
                                            "Not Deleted!",
                                            "Something went wrong",
                                            "error"
                                        )
                                    }
                                });
                            }
                        });                
                    }
                }
			],
            headerCallback: function (thead, data, start, end, display) {
                thead.getElementsByTagName('th')[0].innerHTML = `
                    <label class="checkbox checkbox-single checkbox-solid checkbox-primary mb-0">
                        <input type="checkbox" value="" class="group-checkable"/>
                        <span></span>
                    </label>`;
            },
            "processing": true,
            "serverSide": true,
            "ajax": BASE_URL + "/api/accounting/list-income-category/",
            "columnDefs": [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, full, meta) {
                        return `
                        <label class="checkbox checkbox-single checkbox-primary mb-0">
                        <input type="checkbox" value="" class="checkable"/>
                        <span></span>
                        </label>`;
                    },
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return '<a href="/accounting/update-income-category/' + row[0] + '" class="btn btn-sm btn-clean btn-icon" title="Edit details"><i class="far fa-edit"></i></a><a href="/api/accounting/incomecategory/delete/'+row[0]+'/" class="btn btn-sm btn-clean btn-icon delete-record" title="Delete"><i class="far fa-trash-alt"></i></a>';
                    },
                }
            ],
            "order": [[0, "desc"]],
        });

		income_category_table.on('change', '.group-checkable', function() {
			var set = $(this).closest('table').find('td:first-child .checkable');
			var checked = $(this).is(':checked');

			$(set).each(function() {
				if (checked) {
					$(this).prop('checked', true);
					income_category_table.api().rows($(this).closest('tr')).select();
				}
				else {
					$(this).prop('checked', false);
					income_category_table.api().rows($(this).closest('tr')).deselect();
				}
			});
		});
    }

    if (document.location.href.includes("expense-category")) {
        var expense_category_table = $('.table-expense-category').dataTable({
            stateSave: true,
            stateSave: true,
            select: {
                style: 'multi',
                selector: 'td:first-child .checkable',
            },
			dom: `<'row'<'col-sm-6 text-left'f><'col-sm-6 text-right'B>>
			<'row'<'col-sm-12'tr>>
			<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,

			buttons: [
                {
                    text: "Export to Excel",
                    action: () => {
                        window.location.href = '/accounting/export-expense-category/';
                    }
                },
				{
                    text: 'Delete selected data',
                    action: function () {
                        Swal.fire({
                            title: "Are you sure?",
                            text: "You won't be able to revert this!",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonText: "Yes, delete it!"
                        }).then(function (result) {
                            if (result.value) {
                                const csrftoken = getCookie('csrftoken');
                                let pk_array = $.map(expense_category_table.api().rows( { selected: true } ).data(), function (item) {
                                    return item[0];
                                });
                                $.ajax({
                                    url: '/api/accounting/bulk-delete/',
                                    method: "delete",
                                    data: {
                                        model_name: "ExpenseCategoryModel",
                                        pk_array
                                    },        
                                    headers: {
                                        'X-CSRFTOKEN': csrftoken
                                    },
                                    success: function (response) {
                                        Swal.fire(
                                            "Deleted!",
                                            response.message,
                                            "success"
                                        ).then(function () {
                                            expense_category_table.api().ajax.reload();
                                        });
                                    },
                                    error: function (error) {
                                        Swal.fire(
                                            "Not Deleted!",
                                            "Something went wrong",
                                            "error"
                                        )
                                    }
                                });
                            }
                        });                
                    }
                }
			],
            headerCallback: function (thead, data, start, end, display) {
                thead.getElementsByTagName('th')[0].innerHTML = `
                    <label class="checkbox checkbox-single checkbox-solid checkbox-primary mb-0">
                        <input type="checkbox" value="" class="group-checkable"/>
                        <span></span>
                    </label>`;
            },  
            "processing": true,
            "serverSide": true,
            "ajax": BASE_URL + "/api/accounting/list-expense-category/",
            "columnDefs": [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, full, meta) {
                        return `
                        <label class="checkbox checkbox-single checkbox-primary mb-0">
                        <input type="checkbox" value="" class="checkable"/>
                        <span></span>
                        </label>`;
                    },
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return '<a href="/accounting/update-expense-category/' + row[0] + '" class="btn btn-sm btn-clean btn-icon" title="Edit details"><i class="far fa-edit"></i></a><a href="/api/accounting/expensecategory/delete/'+row[0]+'/" class="btn btn-sm btn-clean btn-icon delete-record" title="Delete"><i class="far fa-trash-alt"></i></a>';
                    },
                }
            ],
            "order": [[0, "desc"]],
        });

		expense_category_table.on('change', '.group-checkable', function() {
			var set = $(this).closest('table').find('td:first-child .checkable');
			var checked = $(this).is(':checked');

			$(set).each(function() {
				if (checked) {
					$(this).prop('checked', true);
					expense_category_table.api().rows($(this).closest('tr')).select();
				}
				else {
					$(this).prop('checked', false);
					expense_category_table.api().rows($(this).closest('tr')).deselect();
				}
			});
		});

    }

    if (document.location.href.includes("members-vendor")) {
        var members_vendor_table = $('.table-members-vendor').dataTable({
            stateSave: true,
            select: {
                style: 'multi',
                selector: 'td:first-child .checkable',
            },
			dom: `<'row'<'col-sm-6 text-left'f><'col-sm-6 text-right'B>>
			<'row'<'col-sm-12'tr>>
			<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,

			buttons: [
                {
                    text: "Export to Excel",
                    action: () => {
                        window.location.href = '/accounting/export-members-vendor/';
                    }
                },
				{
                    text: 'Delete selected data',
                    action: function () {
                        Swal.fire({
                            title: "Are you sure?",
                            text: "You won't be able to revert this!",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonText: "Yes, delete it!"
                        }).then(function (result) {
                            if (result.value) {
                                const csrftoken = getCookie('csrftoken');
                                let pk_array = $.map(members_vendor_table.api().rows( { selected: true } ).data(), function (item) {
                                    return item[0];
                                });
                                $.ajax({
                                    url: '/api/accounting/bulk-delete/',
                                    method: "delete",
                                    data: {
                                        model_name: "MemberVenderDetailModel",
                                        pk_array
                                    },        
                                    headers: {
                                        'X-CSRFTOKEN': csrftoken
                                    },
                                    success: function (response) {
                                        Swal.fire(
                                            "Deleted!",
                                            response.message,
                                            "success"
                                        ).then(function () {
                                            members_vendor_table.api().ajax.reload();
                                        });
                                    },
                                    error: function (error) {
                                        Swal.fire(
                                            "Not Deleted!",
                                            "Something went wrong",
                                            "error"
                                        )
                                    }
                                });
                            }
                        });                
                    }
                }
			],
            headerCallback: function (thead, data, start, end, display) {
                thead.getElementsByTagName('th')[0].innerHTML = `
                    <label class="checkbox checkbox-single checkbox-solid checkbox-primary mb-0">
                        <input type="checkbox" value="" class="group-checkable"/>
                        <span></span>
                    </label>`;
            },
            "processing": true,
            "serverSide": true,
            "ajax": BASE_URL + "/api/accounting/list-members-vendor/",
            "columnDefs": [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, full, meta) {
                        return `
                        <label class="checkbox checkbox-single checkbox-primary mb-0">
                        <input type="checkbox" value="" class="checkable"/>
                        <span></span>
                        </label>`;
                    },
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return '<a href="/accounting/update-members-vendor/' + row[0] + '" class="btn btn-sm btn-clean btn-icon" title="Edit details"><i class="far fa-edit"></i></a><a href="/api/accounting/membersvender/delete/'+row[0]+'/" class="btn btn-sm btn-clean btn-icon delete-record" title="Delete"><i class="far fa-trash-alt"></i></a>';
                    },
                }
            ],
            "order": [[0, "desc"]],
        });

		members_vendor_table.on('change', '.group-checkable', function() {
			var set = $(this).closest('table').find('td:first-child .checkable');
			var checked = $(this).is(':checked');

			$(set).each(function() {
				if (checked) {
					$(this).prop('checked', true);
					members_vendor_table.api().rows($(this).closest('tr')).select();
				}
				else {
					$(this).prop('checked', false);
					members_vendor_table.api().rows($(this).closest('tr')).deselect();
				}
			});
		});
    }

    if (document.location.href.includes("member-details")) {
        var members_details_table = $('.table-member-details').dataTable({
            stateSave: true,
            "processing": true,
            select: {
                style: 'multi',
                selector: 'td:first-child .checkable',
            },
			dom: `<'row'<'col-sm-6 text-left'f><'col-sm-6 text-right'B>>
			<'row'<'col-sm-12'tr>>
			<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,

			buttons: [
                {
                    text: "Export to Excel",
                    action: () => {
                        window.location.href = '/accounting/export-member-details/';
                    }
                },
				{
                    text: 'Delete selected data',
                    action: function () {
                        Swal.fire({
                            title: "Are you sure?",
                            text: "You won't be able to revert this!",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonText: "Yes, delete it!"
                        }).then(function (result) {
                            if (result.value) {
                                const csrftoken = getCookie('csrftoken');
                                let pk_array = $.map(members_details_table.api().rows( { selected: true } ).data(), function (item) {
                                    return item[0];
                                });
                                $.ajax({
                                    url: '/api/accounting/bulk-delete/',
                                    method: "delete",
                                    data: {
                                        model_name: "SocietyMemberDetailsModel",
                                        pk_array
                                    },        
                                    headers: {
                                        'X-CSRFTOKEN': csrftoken
                                    },
                                    success: function (response) {
                                        Swal.fire(
                                            "Deleted!",
                                            response.message,
                                            "success"
                                        ).then(function () {
                                            members_details_table.api().ajax.reload();
                                        });
                                    },
                                    error: function (error) {
                                        Swal.fire(
                                            "Not Deleted!",
                                            "Something went wrong",
                                            "error"
                                        )
                                    }
                                });
                            }
                        });                
                    }
                }
			],
            headerCallback: function (thead, data, start, end, display) {
                thead.getElementsByTagName('th')[0].innerHTML = `
                    <label class="checkbox checkbox-single checkbox-solid checkbox-primary mb-0">
                        <input type="checkbox" value="" class="group-checkable"/>
                        <span></span>
                    </label>`;
            },
            "serverSide": true,
            "ajax": BASE_URL + "/api/accounting/list-members-details/",
            "columnDefs": [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, full, meta) {
                        return `
                        <label class="checkbox checkbox-single checkbox-primary mb-0">
                        <input type="checkbox" value="" class="checkable"/>
                        <span></span>
                        </label>`;
                    },
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return '<a href="/accounting/update-member-details/' + row[0] + '" class="btn btn-sm btn-clean btn-icon" title="Edit details"><i class="far fa-edit"></i></a><a href="/api/accounting/memberdetails/delete/'+row[0]+'/" class="btn btn-sm btn-clean btn-icon delete-record" title="Delete"><i class="far fa-trash-alt"></i></a>';
                    },
                }
            ],
            "order": [[0, "desc"]],
        });

		members_details_table.on('change', '.group-checkable', function() {
			var set = $(this).closest('table').find('td:first-child .checkable');
			var checked = $(this).is(':checked');

			$(set).each(function() {
				if (checked) {
					$(this).prop('checked', true);
					members_details_table.api().rows($(this).closest('tr')).select();
				}
				else {
					$(this).prop('checked', false);
					members_details_table.api().rows($(this).closest('tr')).deselect();
				}
			});
		});
    }

    if (document.location.href.includes("balance")) {
        var balance_table = $('.table-balance').dataTable({
            stateSave: true,
            select: {
                style: 'multi',
                selector: 'td:first-child .checkable',
            },
			dom: `<'row'<'col-sm-6 text-left'f><'col-sm-6 text-right'B>>
			<'row'<'col-sm-12'tr>>
			<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,

			buttons: [
				{
                    text: 'Delete selected data',
                    action: function () {
                        Swal.fire({
                            title: "Are you sure?",
                            text: "You won't be able to revert this!",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonText: "Yes, delete it!"
                        }).then(function (result) {
                            if (result.value) {
                                const csrftoken = getCookie('csrftoken');
                                let pk_array = $.map(balance_table.api().rows( { selected: true } ).data(), function (item) {
                                    return item[0];
                                });
                                $.ajax({
                                    url: '/api/accounting/bulk-delete/',
                                    method: "delete",
                                    data: {
                                        model_name: "BalanceModel",
                                        pk_array
                                    },        
                                    headers: {
                                        'X-CSRFTOKEN': csrftoken
                                    },
                                    success: function (response) {
                                        Swal.fire(
                                            "Deleted!",
                                            response.message,
                                            "success"
                                        ).then(function () {
                                            balance_table.api().ajax.reload();
                                        });
                                    },
                                    error: function (error) {
                                        Swal.fire(
                                            "Not Deleted!",
                                            "Something went wrong",
                                            "error"
                                        )
                                    }
                                });
                            }
                        });                
                    }
                }
			],
            headerCallback: function (thead, data, start, end, display) {
                thead.getElementsByTagName('th')[0].innerHTML = `
                    <label class="checkbox checkbox-single checkbox-solid checkbox-primary mb-0">
                        <input type="checkbox" value="" class="group-checkable"/>
                        <span></span>
                    </label>`;
            },
            "processing": true,
            "serverSide": true,
            "ajax": BASE_URL + "/api/accounting/list-balance/",
            "columnDefs": [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, full, meta) {
                        return `
                        <label class="checkbox checkbox-single checkbox-primary mb-0">
                        <input type="checkbox" value="" class="checkable"/>
                        <span></span>
                        </label>`;
                    },
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return '<a href="/accounting/update-balance/' + row[0] + '" class="btn btn-sm btn-clean btn-icon" title="Edit details"><i class="far fa-edit"></i></a><a href="/api/accounting/balance/delete/'+row[0]+'/" class="btn btn-sm btn-clean btn-icon delete-record" title="Delete"><i class="far fa-trash-alt"></i></a>';
                    },
                }
            ],
            "order": [[0, "desc"]],
        });

		balance_table.on('change', '.group-checkable', function() {
			var set = $(this).closest('table').find('td:first-child .checkable');
			var checked = $(this).is(':checked');

			$(set).each(function() {
				if (checked) {
					$(this).prop('checked', true);
					balance_table.api().rows($(this).closest('tr')).select();
				}
				else {
					$(this).prop('checked', false);
					balance_table.api().rows($(this).closest('tr')).deselect();
				}
			});
		});

    }

    if (document.location.href.includes("ledger")) {
        var income_expense_ledger = $('.table-income-expense-ledger').dataTable({
            stateSave: true,
            select: {
                style: 'multi',
                selector: 'td:first-child .checkable',
            },
			dom: `<'row'<'col-sm-4 text-left'f><'col-sm-8 text-right'B>>
			<'row'<'col-sm-12'tr>>
			<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7 dataTables_pager'lp>>`,

			buttons: [
                {
                    text: "Cash Withdrawal",
                    action: () => {
                        window.location.href = '/accounting/cash-withdrawal/';
                    }
                },
                {
                    text: "Cash Deposit",
                    action: () => {
                        window.location.href = '/accounting/cash-deposit/';
                    }
                },
                {
                    text: "Export to Excel",
                    action: () => {
                        window.location.href = '/accounting/export-income-expense-ledger/';
                    }
                },
				{
                    text: 'Delete selected data',
                    action: function () {
                        Swal.fire({
                            title: "Are you sure?",
                            text: "You won't be able to revert this!",
                            icon: "warning",
                            showCancelButton: true,
                            confirmButtonText: "Yes, delete it!"
                        }).then(function (result) {
                            if (result.value) {
                                const csrftoken = getCookie('csrftoken');
                                let pk_array = $.map(income_expense_ledger.api().rows( { selected: true } ).data(), function (item) {
                                    return item[0];
                                });
                                $.ajax({
                                    url: '/api/accounting/bulk-delete/',
                                    method: "delete",
                                    data: {
                                        model_name: "IncomeExpenseLedgerModel",
                                        pk_array
                                    },        
                                    headers: {
                                        'X-CSRFTOKEN': csrftoken
                                    },
                                    success: function (response) {
                                        Swal.fire(
                                            "Deleted!",
                                            response.message,
                                            "success"
                                        ).then(function () {
                                            income_expense_ledger.api().ajax.reload();
                                        });
                                    },
                                    error: function (error) {
                                        Swal.fire(
                                            "Not Deleted!",
                                            "Something went wrong",
                                            "error"
                                        )
                                    }
                                });
                            }
                        });                
                    }
                }
			],
            headerCallback: function (thead, data, start, end, display) {
                thead.getElementsByTagName('th')[0].innerHTML = `
                    <label class="checkbox checkbox-single checkbox-solid checkbox-primary mb-0">
                        <input type="checkbox" value="" class="group-checkable"/>
                        <span></span>
                    </label>`;
            },
            "processing": true,
            "serverSide": true,
            "ajax": BASE_URL + "/api/accounting/list-income-expense-ledger/",
            "columnDefs": [
                {
                    targets: 0,
                    orderable: false,
                    render: function (data, type, full, meta) {
                        return `
                        <label class="checkbox checkbox-single checkbox-primary mb-0">
                        <input type="checkbox" value="" class="checkable"/>
                        <span></span>
                        </label>`;
                    },
                },
                {
                    targets: 9,
                    orderable: false,
                    render: function (data, type, row, meta) {
                        if(!row[9]){
                            return '<a href="/accounting/upload-ledger-file/' + row[0] + '" class="btn btn-primary">File</a>';
                        }else{
                            return '<a href="'+row[9]+'">open file</a>'
                        }
                    },
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        return '<a href="/accounting/update-income-expense-ledger/' + row[0] + '" class="btn btn-sm btn-clean btn-icon" title="Edit details"><i class="far fa-edit"></i></a><a href="/api/accounting/incomeexpenseledger/delete/'+row[0]+'/" class="btn btn-sm btn-clean btn-icon delete-record" title="Delete"><i class="far fa-trash-alt"></i></a>';
                    },
                }
            ],
            "order": [[0, "desc"]],
        });

		income_expense_ledger.on('change', '.group-checkable', function() {
			var set = $(this).closest('table').find('td:first-child .checkable');
			var checked = $(this).is(':checked');

			$(set).each(function() {
				if (checked) {
					$(this).prop('checked', true);
					income_expense_ledger.api().rows($(this).closest('tr')).select();
				}
				else {
					$(this).prop('checked', false);
					income_expense_ledger.api().rows($(this).closest('tr')).deselect();
				}
			});
		});
    }

})