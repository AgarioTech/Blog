let activeElement = null

function splitContent(value) {
    const paragraphs = value.split('</p>');
    const first = paragraphs[0] + '</p>';

    const text = first.replace(/<.*?>/g, '');

    if (text.length <= 300) {
        return first;
    } else {
        return '';
    }
}


function smart_time(date) {
    const result = Date.now() - new Date(date).getTime()
    const seconds = Math.floor(result / 1000)
    const minutes = Math.floor(seconds / 60)
    const hours = Math.floor(seconds / 3600)
    const days = Math.floor( hours / 24)


    if (days > 0) {
        return new Date(date).toLocaleString('ru-Ru', {
            day: 'numeric',
            month: 'long',
        })
    }

    if (hours > 0) {
        return `${hours} ч назад`
    } else {
        if (minutes < 1) {
            return `${seconds} с назад`
        } else {
            return `${minutes} мин назад`
        }
    }
}

function smart_word_end(number) {
    if (number % 10 === 11 || number % 10 === 14) {
        return 'комментариев'
    } else {
        if (number % 10 === 1) {
            return 'комментарий'
        } else if (number % 10 === 2 || number % 10 === 4) {
            return 'комментария'
        } else {
            return 'комментариев'
        }
    }
}



async function setFilter(element) {
    const elements = document.querySelectorAll('.filters__filter-option')
    if (element.classList.contains('selected')) {
        element.classList.remove('selected')
        window.postType = null
    } else {
        elements.forEach(el => el.classList.remove('selected'))
        element.classList.add('selected')
        window.postFilter = element.textContent
    }
}



function moveArrow() {
    const lentaButton = document.querySelector('.filters__arrow')
    const filtersContainer = document.querySelector('.filters')
    if (lentaButton.classList.contains('filters__arrow--down')) {
        lentaButton.classList.remove('filters__arrow--down')
        filtersContainer.style.height = 'auto'
        filtersContainer.style.padding = '25px 25px 15px 25px'
    } else {
        lentaButton.classList.add('filters__arrow--down')
        filtersContainer.style.height = '20px'
        filtersContainer.style.overflow = 'hidden'
        filtersContainer.style.padding = '25px 25px 25px 25px'
    }
}