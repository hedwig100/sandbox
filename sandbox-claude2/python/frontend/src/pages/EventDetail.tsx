import { useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { api } from "@/api/client"

export default function EventDetail() {
  const { id } = useParams<{ id: string }>()

  const { data: event, isLoading } = useQuery({
    queryKey: ["event", id],
    queryFn: () => api.events.get(id!),
    enabled: !!id,
  })

  if (isLoading) return <div className="container mx-auto py-8">読み込み中...</div>
  if (!event) return <div className="container mx-auto py-8">イベントが見つかりません</div>

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle>{event.name}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground mb-4">{event.description}</p>
          <div className="text-sm text-muted-foreground">
            作成日時: {new Date(event.created_at).toLocaleString("ja-JP")}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
