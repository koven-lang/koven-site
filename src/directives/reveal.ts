import type {Directive} from 'vue'

// v-reveal / v-reveal="120"：进入视口时淡入上移，参数为延迟毫秒
const io: IntersectionObserver | null =
    typeof IntersectionObserver === 'undefined'
        ? null
        : new IntersectionObserver((entries, ob) => {
            for (const e of entries) if (e.isIntersecting) {
                e.target.classList.add('in');
                ob.unobserve(e.target)
            }
        }, {threshold: 0.12})

export const reveal: Directive<HTMLElement, number | undefined> = {
    mounted(el, b) {
        el.classList.add('reveal')
        if (b.value) el.style.transitionDelay = `${b.value}ms`
        io ? io.observe(el) : el.classList.add('in')
    },
}
