"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { CheckCircle } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

export default function ConfirmationScreen() {
  const router = useRouter()

  // Auto-focus the continue button for keyboard users
  useEffect(() => {
    const button = document.getElementById("continue-button")
    if (button) button.focus()
  }, [])

  return (
    <div className="min-h-screen w-full bg-background p-4">
      <div className="mx-auto max-w-[500px] space-y-6">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
            <span className="text-lg font-bold text-primary-foreground">TT</span>
          </div>
        </div>

        {/* Success Card */}
        <Card className="flex flex-col items-center space-y-6 p-8 text-center">
          {/* Animated Check Icon */}
          <div className="relative">
            <div className="absolute -inset-4 animate-pulse rounded-full bg-green-100" />
            <CheckCircle className="relative h-24 w-24 text-green-500" />
          </div>

          {/* Success Message */}
          <div className="space-y-2">
            <h1 className="text-2xl font-bold tracking-tight">Account Created!</h1>
            <p className="text-muted-foreground">
              Welcome to our job agency platform. Your profile has been successfully set up.
            </p>
          </div>

          {/* Summary */}
          <div className="w-full space-y-2 rounded-lg bg-muted p-4 text-left">
            <p className="text-sm font-medium">Completed Steps:</p>
            <ul className="text-sm text-muted-foreground">
              <li className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Account registration</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Interest selection</span>
              </li>
              <li className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>Profile verification</span>
              </li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex w-full flex-col gap-2">
            <Button id="continue-button" size="lg" className="w-full" onClick={() => router.push("/dashboard")}>
              Continue to Dashboard
            </Button>
            <Button variant="outline" size="lg" className="w-full" onClick={() => router.push("/profile")}>
              Complete Your Profile
            </Button>
          </div>
        </Card>

        {/* Help Text */}
        <p className="text-center text-sm text-muted-foreground">
          Need help?{" "}
          <Button variant="link" className="p-0 text-sm" onClick={() => router.push("/support")}>
            Contact support
          </Button>
        </p>
      </div>
    </div>
  )
}

