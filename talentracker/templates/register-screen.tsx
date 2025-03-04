"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function RegisterScreen() {
  const router = useRouter()
  const [error, setError] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const form = e.target as HTMLFormElement
    const password = form.password.value
    const confirmPassword = form.confirmPassword.value

    if (password !== confirmPassword) {
      setError("Passwords do not match")
      return
    }

    // Handle registration logic here
    setError("")
  }

  return (
    <div className="min-h-screen w-full bg-background p-4">
      <div className="mx-auto max-w-[450px] space-y-6">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
            <span className="text-lg font-bold text-primary-foreground">TT</span>
          </div>
        </div>

        <div className="space-y-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">Registration</h1>
          <p className="text-sm text-muted-foreground">Create your account to get started</p>
        </div>

        {/* Registration Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label htmlFor="firstName">First Name</Label>
              <Input id="firstName" placeholder="Enter your first name" required />
            </div>
            <div className="space-y-2">
              <Label htmlFor="lastName">Last Name</Label>
              <Input id="lastName" placeholder="Enter your last name" required />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" placeholder="Enter your email" required />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" placeholder="Create a password" required />
          </div>

          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input id="confirmPassword" type="password" placeholder="Confirm your password" required />
          </div>

          {error && <p className="text-sm text-red-500">{error}</p>}

          {/* Register Button */}
          <Button className="w-full" size="lg" type="submit">
            Register
          </Button>

          {/* Login Link */}
          <div className="text-center">
            <Button variant="link" className="text-sm" onClick={() => router.push("/login")}>
              Already have an account? Login here
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

