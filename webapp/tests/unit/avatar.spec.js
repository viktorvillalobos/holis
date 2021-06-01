import { shallowMount } from '@vue/test-utils'
import Avatar from '@/components/Avatar.vue'

describe('Avatar.vue', () => {
  it('renders props.img when passed', () => {
    const img = 'https://hol.is/media/avatar.png'
    const wrapper = shallowMount(Avatar, {
      propsData: { img }
    })


    console.log(wrapper.props())
    expect(wrapper.props().img).toMatch(img)
  })
})
