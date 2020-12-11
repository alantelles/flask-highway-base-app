try {
    const $delBtn = document.getElementById('deleteButton')
    $delBtn.addEventListener('click', function() {
        const del_route = this.dataset.route
        Swal.fire({
            title: 'Are you sure?',
            text: "You are about to delete this record. You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(del_route, {method: 'DELETE'})
                .then(resp => resp.json())
                .then(data => {
                    const message = data['message']
                    const redir = data['redirect'] ? data['redirect'] : '/'
                    window.location.replace(redir)
                })
                .catch(err => {
                    Swal.fire(
                        'Oops!',
                        'Something went wrong. No operation has been done.',
                        'error'
                    )
                })
            }
        })
            
    })
}
catch {
    console.log('No delete button on this page')
}