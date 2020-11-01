import { Extension, Plugin } from 'tiptap'

export class EnterHandler extends Extension {
  get name () {
    return 'enter_handler'
  }

  get plugins () {
    return [
      new Plugin({
        props: {
          handleKeyDown: (view, event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
              // do something
              if (window.$chatEditor.isSendActive) {
                window.$chatEditor.submit()
              }
              return true
            }
            return false
          }
        }
      })
    ]
  }
}
