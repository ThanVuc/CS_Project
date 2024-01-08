window.onpopstate = function (event) {
    if (event.state) {
        if (event.state.id === undefined) {
            if (event.state.mailbox === 'compose') {
                loadCompose();
            } else if (event.state.mailbox === 'Inbox' || event.state.mailbox === 'Sent' || event.state.mailbox === 'Archived') {
                loadMailBox(event.state.mailbox);
            }
        } else {
            console.log(event.state.mailbox);
            if (event.state.id >= '0' && event.state.id <= '9') {
                detail_getAndHandleAPI(parseInt(event.state.id), event.state.mailbox);
            }
        }
    }
}

var hasrun = true;
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#oldmail-block').style.display = 'none';
    document.querySelector('#Inbox').onclick = () => {
        history.pushState({ mailbox: 'Inbox' }, "", "home%2Finbox");
        loadMailBox('Inbox');
    }
    document.querySelector('#Sent').onclick = () => {
        history.pushState({ mailbox: 'Sent' }, "", "home%2Fsent");
        loadMailBox('Sent');
    }
    document.querySelector('#Archived').onclick = () => {
        history.pushState({ mailbox: 'Archived' }, "", "home%2Farchived");
        loadMailBox('Archived');
    }
    document.querySelector('#Compose').onclick = () => {
        history.pushState({ mailbox: 'compose' }, "", "home%2Fcompose");
        loadCompose();
    }

    document.querySelector('#compose-form').onsubmit = function () {
        postToEmail();
        history.pushState({ mailbox: 'Sent' }, "", "home%2Fsent");
        setTimeout(() => loadMailBox('Sent'), 300);
        return false;
    }




    let observer = new MutationObserver(function () {
        document.querySelectorAll('.mail-link').forEach(mail => {
            mail.onclick = function () {
                detail_showDetail(mail.dataset.mailbox, mail.dataset.id);
            }
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
});


function loadCompose() {
    document.querySelector('#mailBox').style.display = 'none';
    document.querySelector('#compose').style.display = 'block';
    document.querySelector('#detailview').style.display = 'none';

    document.querySelector('#recipients').value = '';
    document.querySelector('#subject').value = '';
    document.querySelector('#body').value = '';
    document.querySelector('#bt-oldmail').style.display = 'none';
    document.querySelector('#oldmail-block').style.display = 'none';
}

function loadMailBox(mailbox) {

    if (hasrun) {
        if (mailbox == "Inbox") {
            history.pushState({ mailbox: 'Inbox', id: '-1' }, "", `home%2Finbox`);
        }
        hasrun = false;
    }

    document.querySelector('#mailBox').style.display = 'block';
    document.querySelector('#compose').style.display = 'none';
    document.querySelector('#detailview').style.display = 'none';
    document.querySelector('#mailBox').innerHTML = `<h3 class="mt-3 mb-3">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    mailBox_addEmailToBox(mailbox.toLowerCase());
}

function postToEmail() {
    let data = {
        recipients: document.querySelector('#recipients').value,
        subject: document.querySelector('#subject').value,
        body: document.querySelector('#body').value
    }
    let option = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }
    fetch('/emails', option)
}

let listEmails;
let thisPage = 1, limit = 7;
function mailBox_addEmailToBox(mailbox) {
    url = `/emails/${mailbox}`;
    fetch(url)
        .then(response => response.json())
        .then(emails => {
            mailBox_addEmailToHTMLDiv(emails, mailbox);
            listEmails = document.querySelectorAll('.mail-link');
            paging_loadEmail();
        })

}

function mailBox_addEmailToHTMLDiv(emails, mailbox) {
    emails.forEach(email => {
        let element = document.createElement('div');
        let sender = email.sender, subject = email.subject, timestamp = email.timestamp, read = email.read;
        let id = email.id;
        element.innerHTML = `<div class="d-flex w-75"> <p style="width: 10%; font-weight: bold; text-align: left;">${sender}</p> <p class="w-50">${subject}</p> </div> <p>${timestamp}</p>`;
        element.className = 'mail-link d-flex justify-content-between border border-dark pt-2 ps-2 pe-2 btn btn-outline-dark mb-2';
        if (read) {
            element.classList.add('bg-color');
        }
        element.dataset.id = id;
        element.dataset.mailbox = mailbox;
        document.querySelector('#mailBox').append(element);
    });
    let listPageTag = document.createElement('div');
    listPageTag.className = 'pagination';
    document.querySelector('#mailBox').append(listPageTag);
}

function detail_showDetail(mailbox, id) {
    history.pushState({ mailbox: `${mailbox}`, id: `${id}` }, "", `mail%2F${id}`);
    detail_getAndHandleAPI(id, mailbox);
}

function detail_getAndHandleAPI(id, mailbox) {
    url = `/emails/${id}`;
    console.log(id);

    fetch(url)
        .then(response => response.json())
        .then(email => {
            document.querySelector('#compose').style.display = 'none';
            document.querySelector('#mailBox').style.display = 'none';
            document.querySelector('#detailview').style.display = 'block';
            const archived = email.archived;
            if (mailbox != 'Sent') {
                if (!archived) {
                    document.querySelector('#detailview').innerHTML = `<div class="d-flex justify-content-between mt-3 mb-3"> 
            <h3>Email</h3> 
            <button id="archived" class="btn btn-outline-success ms-auto" data-id="${id} data-archived="${archived}">Arichived</button>`;

                } else {
                    document.querySelector('#detailview').innerHTML = `<div class="d-flex justify-content-between mt-3 mb-3"> 
            <h3>Email</h3> 
            <button id="archived" class="btn btn-outline-danger ms-auto" data-id="${id} data-archived="${archived}"">Unarchived</button>`;
                }

                document.querySelector('#archived').onclick = () => {
                    const archived = email.archived;
                    const archived_status = {
                        archived: !archived
                    }
                    const archived_option = {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(archived_status)
                    }
                    fetch(url, archived_option)
                    history.pushState({ mailbox: 'Inbox' }, "", "home%2Finbox");

                    setTimeout(() => loadMailBox('Inbox'), 300);
                }

            } else {
                document.querySelector('#detailview').innerHTML = `<h3 class="mt-3 mb-3">Email</h3>`;
            }

            let element = document.createElement('div');
            const sender = email.sender, subject = email.subject,
                timestamp = email.timestamp,
                recipients = email.recipients,
                body = email.body;
            console.log(email);
            element.innerHTML = `<div class="container border-top border-secondary pt-3">
            <div class="d-flex w-100"><p class="frame">From: </p> <p>${sender}</p></div>
            <div class="d-flex w-100"><p class="frame">To: <p>${recipients}</p></div>
            <div class="d-flex w-100"><p class="frame">Subject: </p> <p>${subject}</p></div>
            <div class="d-flex w-100"><p class="frame">Timestamp: </p> <p>${timestamp}</p></div>
            <div><button id="reply" class="btn btn-outline-primary">Reply</button>
        </div>
        <p class="container border-top border-secondary mt-3 pt-2">${body}</p>`;
            element.className = 'mail-detail';
            document.querySelector('#detailview').append(element);

            document.querySelector('#reply').onclick = () => {
                history.pushState({ mailbox: 'compose' }, "", "home%2Fcompose");
                loadCompose();
                reply_handle(sender, subject, body, timestamp);
            }
        })

    change_read_status(url);
}

function change_read_status(url) {
    const read_status = {
        read: true
    }
    const read_option = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(read_status)
    }
    fetch(url, read_option)
}

function reply_handle(sender, subject, body, timestamp) {
    let bt = document.querySelector('#bt-oldmail');
    let oldmail = document.querySelector('#oldmail');
    document.querySelector('#recipients').value = sender;

    if (!subject.startsWith('Re: '))
        document.querySelector('#subject').value = `Re: ${subject}`;
    else
        document.querySelector('#subject').value = `${subject}`;

    oldmail.value = `On ${timestamp} ${sender} wrote: \n ${body}`;
    bt.style.display = 'block';
    bt.onclick = () => {
        var displayOldMail = document.querySelector('#oldmail-block');
        if (displayOldMail.style.display === 'none')
            displayOldMail.style.display = 'block';
        else
            displayOldMail.style.display = 'none';
        return false;
    }
}

function paging_loadEmail() {
    let beginPage = limit * (thisPage - 1);
    let endPage = limit * thisPage - 1;
    listEmails.forEach((mail, key) => {
        if (beginPage <= key && key <= endPage) {
            mail.style.cssText = 'display: flex !important;';
        } else {
            mail.style.cssText = 'display: none !important;';
        }
    })
    listPage();
}

function listPage() {
    let total = Math.ceil(listEmails.length / limit);
    document.querySelector('#mailBox .pagination').innerHTML = "";

    let prev = document.createElement('li');
    if (thisPage > 1) {
        prev.innerHTML = `<li class="page-item"><a class="page-link" href="#" style="border: none;"><i class="fa fa-angle-left"></a></li>`;
        prev.setAttribute("onclick", "changePage(" + (thisPage - 1) + ")");
    } else {
        prev.innerHTML = `<li class="page-item disabled"><a class="page-link" href="#" style="border: none;"><i class="fa fa-angle-left"></a></li>`;
    }

    document.querySelector('#mailBox .pagination').appendChild(prev);

    for (i = 1; i <= total; i++) {
        let newPage = document.createElement('li');
        newPage.innerHTML = `<li class="page-item"><a class="page-link" href="#" style="border: none;">${i}</a></li>`;
        if (i === thisPage) {
            newPage.innerHTML = `<li class="page-item active"><a class="page-link" href="#" style="border: none;">${i}</a></li>`;
        }
        newPage.setAttribute("onclick", "changePage(" + i + ")");
        document.querySelector('#mailBox .pagination').appendChild(newPage);
    }

    let next = document.createElement('li');
    if (thisPage < total) {
        next.innerHTML = `<li class="page-item"><a class="page-link" href="#" style="border: none;"><i class="fa fa-angle-right"></i></a></li>`;
        next.setAttribute("onclick", "changePage(" + (thisPage + 1) + ")");
    } else {
        next.innerHTML = `<li class="page-item disabled"><a class="page-link" href="#" style="border: none;"><i class="fa fa-angle-right"></i></a></li>`;
    }
    document.querySelector('#mailBox .pagination').appendChild(next);
}

function changePage(i) {
    thisPage = i;
    paging_loadEmail();
}

