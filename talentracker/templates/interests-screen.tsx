"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Check, UserCircle } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"

const interests = [
  { id: "tech", label: "Technology", icon: "💻" },
  { id: "finance", label: "Finance", icon: "💰" },
  { id: "healthcare", label: "Healthcare", icon: "🏥" },
  { id: "education", label: "Education", icon: "📚" },
  { id: "marketing", label: "Marketing", icon: "📢" },
  { id: "design", label: "Design", icon: "🎨" },
  { id: "engineering", label: "Engineering", icon: "⚙️" },
  { id: "sales", label: "Sales", icon: "🤝" },
  { id: "hr", label: "Human Resources", icon: "👥" },
  { id: "consulting", label: "Consulting", icon: "💡" },
  { id: "research", label: "Research", icon: "🔬" },
  { id: "writing", label: "Content Writing", icon: "✍️" },
]

export default function InterestsScreen() {
  const router = useRouter()
  const [selectedInterests, setSelectedInterests] = useState<string[]>([])

  const toggleInterest = (id: string) => {
    setSelectedInterests((prev) => (prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (selectedInterests.length < 3) {
      alert("Please select at least 3 interests")
      return
    }
    // Handle submission and navigation
    console.log("Selected interests:", selectedInterests)
    router.push("/dashboard") // Navigate to the next step
  }

  return (
    <div className="min-h-screen w-full bg-background p-4">
      <div className="mx-auto max-w-[800px] space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
              <span className="text-lg font-bold text-primary-foreground">TT</span>
            </div>
          </div>
          <UserCircle className="h-10 w-10 text-muted-foreground" />
        </div>

        {/* Content */}
        <div className="space-y-4">
          <div className="space-y-2">
            <h1 className="text-2xl font-semibold tracking-tight">Personalize Your Experience</h1>
            <p className="text-sm text-muted-foreground">
              Select at least 3 interests to help us personalize your job recommendations
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Interests Grid */}
            <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
              {interests.map((interest) => (
                <Card
                  key={interest.id}
                  className={`group cursor-pointer p-4 transition-colors hover:bg-muted ${
                    selectedInterests.includes(interest.id) ? "border-primary bg-primary/5" : ""
                  }`}
                  onClick={() => toggleInterest(interest.id)}
                >
                  <div className="flex items-center space-x-2">
                    <div className="text-2xl">{interest.icon}</div>
                    <Label className="flex-1 cursor-pointer font-medium">{interest.label}</Label>
                    {selectedInterests.includes(interest.id) && <Check className="h-4 w-4 text-primary" />}
                  </div>
                </Card>
              ))}
            </div>

            {/* Progress and Actions */}
            <div className="flex items-center justify-between">
              <div className="text-sm text-muted-foreground">{selectedInterests.length} of 3 minimum selected</div>
              <Button type="submit" size="lg" disabled={selectedInterests.length < 3}>
                Continue to Verification
              </Button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

