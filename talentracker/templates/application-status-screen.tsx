"use client"

import {
  Building2,
  Calendar,
  CheckCircle,
  Clock,
  Download,
  FileText,
  Mail,
  MapPin,
  MessageSquare,
  Phone,
  UserCircle,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"

// Example application data
const applicationData = {
  jobTitle: "Senior Web Developer",
  company: "TechCorp Solutions",
  location: "San Francisco, CA",
  salary: "$120k - $150k",
  type: "Full-time",
  appliedDate: "Feb 20, 2024",
  currentStep: 2,
  nextStep: {
    title: "Technical Interview",
    date: "March 1, 2024",
    time: "2:00 PM PST",
    description: "60-minute technical discussion with the engineering team",
  },
  progress: 60,
  recruiter: {
    name: "Sarah Johnson",
    role: "Technical Recruiter",
    email: "sarah.j@techcorp.com",
    phone: "(555) 123-4567",
  },
  documents: [
    { name: "Resume", status: "approved" },
    { name: "Cover Letter", status: "approved" },
    { name: "Portfolio", status: "pending" },
  ],
  timeline: [
    {
      date: "Feb 20, 2024",
      title: "Application Submitted",
      description: "Your application has been successfully submitted",
      status: "completed",
    },
    {
      date: "Feb 22, 2024",
      title: "Initial Screening",
      description: "Application reviewed by hiring team",
      status: "completed",
    },
    {
      date: "Feb 24, 2024",
      title: "Technical Interview Scheduled",
      description: "Interview scheduled for March 1st",
      status: "current",
    },
    {
      date: "Pending",
      title: "Technical Interview",
      description: "60-minute technical discussion",
      status: "upcoming",
    },
    {
      date: "Pending",
      title: "Team Interview",
      description: "Meet with the engineering team",
      status: "upcoming",
    },
    {
      date: "Pending",
      title: "Final Decision",
      description: "Application decision",
      status: "upcoming",
    },
  ],
}

const steps = [
  { id: 1, label: "Applied" },
  { id: 2, label: "Screening" },
  { id: 3, label: "Interview" },
  { id: 4, label: "Team Round" },
  { id: 5, label: "Decision" },
]

export default function ApplicationStatusScreen() {
  return (
    <div className="min-h-screen w-full bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
              <span className="text-lg font-bold text-primary-foreground">TT</span>
            </div>
          </div>
          <UserCircle className="h-8 w-8" />
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-6">
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Main Status Section */}
          <div className="space-y-6 lg:col-span-2">
            {/* Job Details */}
            <div>
              <h1 className="text-2xl font-semibold tracking-tight">{applicationData.jobTitle}</h1>
              <div className="mt-2 flex items-center space-x-2 text-muted-foreground">
                <Building2 className="h-4 w-4" />
                <span>{applicationData.company}</span>
                <Separator orientation="vertical" className="h-4" />
                <MapPin className="h-4 w-4" />
                <span>{applicationData.location}</span>
              </div>
            </div>

            {/* Progress Stepper */}
            <Card className="p-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between text-sm">
                  <span>Application Progress</span>
                  <span>{applicationData.progress}%</span>
                </div>
                <Progress value={applicationData.progress} className="h-2" />

                {/* Steps */}
                <div className="relative mt-8 flex justify-between">
                  {steps.map((step, index) => {
                    const isCompleted = step.id < applicationData.currentStep
                    const isCurrent = step.id === applicationData.currentStep
                    return (
                      <div key={step.id} className="flex flex-col items-center">
                        <div
                          className={`flex h-8 w-8 items-center justify-center rounded-full border-2 ${
                            isCompleted
                              ? "border-primary bg-primary text-primary-foreground"
                              : isCurrent
                                ? "border-primary bg-background"
                                : "border-muted bg-background"
                          }`}
                        >
                          {isCompleted ? (
                            <CheckCircle className="h-4 w-4" />
                          ) : (
                            <span className="text-sm">{step.id}</span>
                          )}
                        </div>
                        <span className="mt-2 text-xs">{step.label}</span>
                      </div>
                    )
                  })}
                  <div className="absolute left-0 top-4 -z-10 h-[2px] w-full bg-muted">
                    <div
                      className="h-full bg-primary transition-all duration-500"
                      style={{
                        width: `${((applicationData.currentStep - 1) / (steps.length - 1)) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              </div>
            </Card>

            {/* Timeline */}
            <Card className="p-6">
              <h2 className="mb-4 font-semibold">Application Timeline</h2>
              <div className="space-y-4">
                {applicationData.timeline.map((event, index) => (
                  <div key={index} className="flex gap-4">
                    <div
                      className={`mt-1 h-2 w-2 rounded-full ${
                        event.status === "completed"
                          ? "bg-primary"
                          : event.status === "current"
                            ? "bg-blue-500"
                            : "bg-muted"
                      }`}
                    />
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-medium">{event.title}</span>
                        <span className="text-sm text-muted-foreground">{event.date}</span>
                      </div>
                      <p className="text-sm text-muted-foreground">{event.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Next Step Card */}
            <Card className="p-6">
              <h2 className="font-semibold">Next Step</h2>
              <div className="mt-4 space-y-4">
                <div className="rounded-lg bg-primary/10 p-4">
                  <h3 className="font-medium text-primary">{applicationData.nextStep.title}</h3>
                  <div className="mt-2 space-y-2 text-sm">
                    <div className="flex items-center space-x-2">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      <span>{applicationData.nextStep.date}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Clock className="h-4 w-4 text-muted-foreground" />
                      <span>{applicationData.nextStep.time}</span>
                    </div>
                  </div>
                  <p className="mt-2 text-sm text-muted-foreground">{applicationData.nextStep.description}</p>
                </div>
                <Button className="w-full">Prepare for Interview</Button>
              </div>
            </Card>

            {/* Documents Status */}
            <Card className="p-6">
              <h2 className="font-semibold">Documents</h2>
              <div className="mt-4 space-y-3">
                {applicationData.documents.map((doc, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <FileText className="h-4 w-4 text-muted-foreground" />
                      <span>{doc.name}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={doc.status === "approved" ? "default" : "secondary"}>{doc.status}</Badge>
                      <Button variant="ghost" size="icon">
                        <Download className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            {/* Recruiter Contact */}
            <Card className="p-6">
              <h2 className="font-semibold">Your Recruiter</h2>
              <div className="mt-4 space-y-4">
                <div className="space-y-1">
                  <div className="font-medium">{applicationData.recruiter.name}</div>
                  <div className="text-sm text-muted-foreground">{applicationData.recruiter.role}</div>
                </div>
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start space-x-2">
                    <Mail className="h-4 w-4" />
                    <span>Send Email</span>
                  </Button>
                  <Button variant="outline" className="w-full justify-start space-x-2">
                    <Phone className="h-4 w-4" />
                    <span>Call</span>
                  </Button>
                  <Button variant="outline" className="w-full justify-start space-x-2">
                    <MessageSquare className="h-4 w-4" />
                    <span>Send Message</span>
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </main>
    </div>
  )
}

