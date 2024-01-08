// let thisPage = 1;
// let limit = 2;
// let listEmails;


// document.addEventListener('DOMContentLoaded', async () => {
//     url = '/emails/sent';
//     let response = await fetch(url);
//     const data = await response.json();
//     data.forEach(email => {
//         let element = document.createElement('div');
//         let sender = email.sender, subject = email.subject, timestamp = email.timestamp;
//         element.innerHTML = `<div class="d-flex w-75"> <p style="width: 10%; font-weight: bold; text-align: left;">${sender}</p> <p class="w-50">${subject}</p> </div> <p>${timestamp}</p>`;
//         element.className = 'mail-link d-flex justify-content-between border border-dark pt-2 ps-2 pe-2 btn btn-outline-dark mb-3';

//         document.querySelector('#email').appendChild(element);
//     });

//     listEmails = document.querySelectorAll('.mail-link');
//     loadEmail();


// })

// function loadEmail() {
//     let beginItem = limit * (thisPage - 1);
//     let endItems = limit * thisPage - 1;

//     listEmails.forEach((item, key) => {
//         if (beginItem <= key && key <= endItems) {
//             item.style.cssText = 'display: flex !important;';
//         } else {
//             item.style.cssText = 'display: none !important;';
//         }
//     })
//     listPage();
// }

// function listPage() {
//     let totalPage = Math.ceil(listEmails.length / limit);
//     document.querySelector('.pagination').innerHTML = '';

//     if (thisPage != 1) {
//         let prev = document.createElement('li');
//         prev.innerHTML = `<li class="page-item"><a id="prev" class="page-link" href="#" style="border: none;"><i class="fa fa-angle-left"></i></a></li>`;
//         prev.setAttribute("onclick", "changePage(" + (thisPage - 1) + ")");
//         document.querySelector('.pagination').appendChild(prev);
//     }

    // for (i = 1; i <= totalPage; i++) {
    //     let newPage = document.createElement('li');
    //     newPage.innerHTML = `<li class="page-item"><a class="page-link" href="#" style="border: none;">${i}</a></li>`;
    //     if (i === thisPage) {
    //         newPage.innerHTML = `<li class="page-item active"><a class="page-link" href="#" style="border: none;">${i}</a></li>`;
    //     }
    //     newPage.setAttribute("onclick", "changePage(" + i + ")");
    //     document.querySelector('.pagination').appendChild(newPage);
    // }

//     if (thisPage != totalPage) {
//         let next = document.createElement('li');
//         next.innerHTML = `<li class="page-item"><a id="prev" class="page-link" href="#" style="border: none;"><i class="fa fa-angle-right"></i></a></li>`;
//         next.setAttribute("onclick", "changePage(" + (thisPage + 1) + ")");
//         document.querySelector('.pagination').appendChild(next);
//     }
// }

// function changePage(i) {
//     thisPage = i;
//     loadEmail();
// }













// {/* <li class="page-item"><a id="prev" class="page-link" href="#" style="border: none;"><i class="fa fa-angle-left"></i></a></li>
//             <li class="page-it  em"><a class="page-link" href="#" style="border: none;">1</a></li>
//             <li class="page-item"><a id="next" class="page-link" href="#" style="border: none;"><i class="fa fa-angle-right"></i></a></li> */}

