import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export default function Home() {
  return (
    <div className="container mx-auto py-8 px-4">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Event Scheduler</h1>
        <p className="text-xl text-muted-foreground mb-8">
          イベントの日程調整を簡単に
        </p>
        <Link to="/new">
          <Button>新しいイベントを作成</Button>
        </Link>
      </div>

      <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>簡単作成</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              数クリックでイベントを作成し、候補日を追加できます
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>リアルタイム更新</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              参加者の回答がリアルタイムで反映されます
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>ログイン不要</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              アカウント登録不要で誰でも簡単に参加できます
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
