"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { CheckCircle, ArrowLeft, Building2, MapPin, Mail, Eye } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

// Example application data
const applicationData = {
  jobTitle: "Senior Web Developer",
  company: "TechCorp Solutions",
  location: "San Francisco, CA",
  referenceNumber: "APP-2024-0123",
  appliedDate: new Date().toLocaleDateString(),
}

// Example similar jobs
const similarJobs = [
  {
    id: 1,
    title: "Full Stack Developer",
    company: "Digital Innovations",
    location: "Remote",
  },
  {
    id: 2,
    title: "Frontend Engineer",
    company: "StartUp Inc",
    location: "New York, NY",
  },
]

export default function ApplicationCompleteScreen() {
  const router = useRouter()

  // Auto-focus the "View More Jobs" button for keyboard users
  useEffect(() => {
    const button = document.getElementById("view-more-jobs")
    if (button) button.focus()
  }, [])

  return (
    <div className="min-h-screen w-full bg-background p-4">
      <div className="container mx-auto max-w-3xl space-y-8 pt-8">
        {/* Success Animation */}
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="relative">
            <div className="absolute -inset-4 animate-pulse rounded-full bg-green-100" />
            <CheckCircle className="relative h-24 w-24 text-green-500" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Application Complete!</h1>
          <p className="text-muted-foreground">Your application has been successfully submitted</p>
        </div>

        {/* Application Summary */}
        <Card className="p-6">
          <div className="space-y-4">
            <div className="space-y-2">
              <h2 className="font-semibold">Application Summary</h2>
              <div className="space-y-1 text-sm text-muted-foreground">
                <p className="flex items-center space-x-2">
                  <Building2 className="h-4 w-4" />
                  <span>{applicationData.company}</span>
                </p>
                <p className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4" />
                  <span>{applicationData.location}</span>
                </p>
              </div>
            </div>
            <div className="space-y-2 rounded-lg bg-muted p-4 text-sm">
              <p className="flex items-center justify-between">
                <span>Reference Number:</span>
                <span className="font-mono font-medium">{applicationData.referenceNumber}</span>
              </p>
              <p className="flex items-center justify-between">
                <span>Applied Date:</span>
                <span>{applicationData.appliedDate}</span>
              </p>
            </div>
            <div className="flex items-center space-x-2 rounded-lg bg-primary/10 p-4 text-sm text-primary">
              <Mail className="h-4 w-4" />
              <span>We've sent you a confirmation email with additional details</span>
            </div>
          </div>
        </Card>

        {/* Similar Jobs */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Similar Jobs You Might Like</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {similarJobs.map((job) => (
              <Card
                key={job.id}
                className="flex cursor-pointer items-start space-x-4 p-4 hover:bg-muted"
                onClick={() => router.push(`/jobs/${job.id}`)}
              >
                <div className="space-y-1">
                  <h3 className="font-medium">{job.title}</h3>
                  <p className="text-sm text-muted-foreground">{job.company}</p>
                  <p className="text-sm text-muted-foreground">{job.location}</p>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col gap-4 pt-4 sm:flex-row sm:justify-between">
          <Button variant="outline" className="space-x-2" onClick={() => router.push("/applications")}>
            <Eye className="h-4 w-4" />
            <span>View My Applications</span>
          </Button>
          <div className="flex flex-col gap-2 sm:flex-row">
            <Button variant="outline" className="space-x-2" onClick={() => router.push("/jobs")}>
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Jobs</span>
            </Button>
            <Button id="view-more-jobs" onClick={() => router.push("/jobs/discover")}>
              View More Jobs
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

