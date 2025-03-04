"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { ArrowLeft, Building2, Calendar, Clock, DollarSign, Heart, MapPin, Share2, UserCircle } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

// Example job data
const jobData = {
  id: 1,
  title: "Senior Web Developer",
  company: "TechCorp Solutions",
  location: "San Francisco, CA",
  type: "Full-time",
  posted: "2 days ago",
  salary: "$120k - $150k/year",
  experience: "5+ years",
  department: "Engineering",
  requirements: [
    "Bachelor's degree in Computer Science or related field",
    "5+ years of experience with React and modern JavaScript",
    "Strong understanding of web fundamentals (HTML, CSS, JavaScript)",
    "Experience with Node.js and REST APIs",
    "Familiarity with cloud services (AWS, GCP, or Azure)",
    "Strong problem-solving and analytical skills",
  ],
  responsibilities: [
    "Lead development of web applications using React and Node.js",
    "Mentor junior developers and review code",
    "Collaborate with product and design teams",
    "Optimize application performance",
    "Implement security best practices",
    "Participate in technical architecture discussions",
  ],
  description: `We are seeking a Senior Web Developer to join our growing engineering team. You will be responsible for developing and maintaining web applications, mentoring junior developers, and contributing to technical decisions.

The ideal candidate has a strong background in modern web development, excellent problem-solving skills, and experience working in an agile environment.

We offer competitive benefits including:
• Health, dental, and vision insurance
• 401(k) matching
• Flexible PTO
• Remote work options
• Professional development budget`,
  companyInfo: {
    name: "TechCorp Solutions",
    size: "501-1000 employees",
    industry: "Information Technology",
    founded: "2010",
    description: "TechCorp Solutions is a leading provider of enterprise software solutions...",
  },
}

export default function JobDetailScreen() {
  const router = useRouter()
  const [isSaved, setIsSaved] = useState(false)

  return (
    <div className="min-h-screen w-full bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button variant="ghost" size="icon" onClick={() => router.back()}>
              <ArrowLeft className="h-4 w-4" />
            </Button>
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
          {/* Main Job Information */}
          <div className="space-y-6 lg:col-span-2">
            {/* Job Header */}
            <div className="space-y-4">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <h1 className="text-2xl font-bold tracking-tight md:text-3xl">{jobData.title}</h1>
                  <div className="flex items-center space-x-2 text-muted-foreground">
                    <Building2 className="h-4 w-4" />
                    <span>{jobData.company}</span>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button variant="ghost" size="icon" onClick={() => setIsSaved(!isSaved)}>
                    <Heart className={`h-5 w-5 ${isSaved ? "fill-primary text-primary" : ""}`} />
                    <span className="sr-only">Save job</span>
                  </Button>
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <Share2 className="h-5 w-5" />
                        <span className="sr-only">Share job</span>
                      </Button>
                    </DialogTrigger>
                    <DialogContent>
                      <DialogHeader>
                        <DialogTitle>Share this job</DialogTitle>
                        <DialogDescription>Share this job opportunity with your network</DialogDescription>
                      </DialogHeader>
                      {/* Add share options here */}
                    </DialogContent>
                  </Dialog>
                </div>
              </div>

              {/* Key Details */}
              <Card className="grid gap-4 p-6 sm:grid-cols-2 md:grid-cols-4">
                <div className="flex items-center space-x-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <span>{jobData.location}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                  <span>{jobData.salary}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <span>{jobData.type}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <span>{jobData.posted}</span>
                </div>
              </Card>
            </div>

            {/* Job Content */}
            <div className="space-y-6">
              {/* Requirements */}
              <section className="space-y-4">
                <h2 className="text-xl font-semibold tracking-tight">Requirements</h2>
                <ul className="list-inside list-disc space-y-2 text-muted-foreground">
                  {jobData.requirements.map((req, index) => (
                    <li key={index}>{req}</li>
                  ))}
                </ul>
              </section>

              {/* Responsibilities */}
              <section className="space-y-4">
                <h2 className="text-xl font-semibold tracking-tight">Responsibilities</h2>
                <ul className="list-inside list-disc space-y-2 text-muted-foreground">
                  {jobData.responsibilities.map((resp, index) => (
                    <li key={index}>{resp}</li>
                  ))}
                </ul>
              </section>

              {/* Description */}
              <section className="space-y-4">
                <h2 className="text-xl font-semibold tracking-tight">About the Role</h2>
                <div className="whitespace-pre-line text-muted-foreground">{jobData.description}</div>
              </section>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Apply Button (Sticky) */}
            <div className="sticky top-20 space-y-6">
              <Button size="lg" className="w-full" onClick={() => router.push(`/jobs/${jobData.id}/apply`)}>
                Apply Now
              </Button>

              {/* Company Card */}
              <Card className="p-6">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <h2 className="font-semibold">{jobData.companyInfo.name}</h2>
                    <div className="space-y-1 text-sm text-muted-foreground">
                      <p>Size: {jobData.companyInfo.size}</p>
                      <p>Industry: {jobData.companyInfo.industry}</p>
                      <p>Founded: {jobData.companyInfo.founded}</p>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">{jobData.companyInfo.description}</p>
                  <Button variant="outline" className="w-full">
                    View Company Profile
                  </Button>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

