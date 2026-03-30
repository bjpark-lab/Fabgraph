import { Button } from '@/shared/ui/button'

export function ConversationHistory({ onLoad: _onLoad }: { onLoad: (conversationId: string) => void }) {
  return (
    <Button
      type="button"
      title="TODO: implement persisted conversation history"
      disabled
    >
      History
    </Button>
  )
}
