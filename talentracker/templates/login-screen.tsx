"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { UserCircle } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function LoginScreen() {
  const router = useRouter()

  return (
    <div className="min-h-screen w-full bg-background p-4">
      <div className="mx-auto max-w-[350px] space-y-6">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
            <span className="text-lg font-bold text-primary-foreground">TT</span>
          </div>
        </div>

        {/* User Icon */}
        <div className="flex justify-center">
          <UserCircle className="h-24 w-24 text-muted-foreground" />
        </div>

        {/* Login Form */}
        <form className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username">Username</Label>
            <Input id="username" placeholder="Enter your username" required type="text" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" placeholder="Enter your password" required type="password" />
          </div>

          {/* Support Link */}
          <div className="text-center">
            <Link href="/support" className="text-sm text-muted-foreground hover:text-primary">
              Need support?
            </Link>
          </div>

          {/* Login Button */}
          <Button className="w-full" size="lg" type="submit">
            Login
          </Button>

          {/* Register Link */}
          <div className="text-center">
            <Button variant="link" className="text-sm" onClick={() => router.push("/register")}>
              Don't have an account? Register here
            </Button>
          </div>
        </form>
      </div>
    </div>
  )
}

