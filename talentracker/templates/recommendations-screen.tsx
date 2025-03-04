"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Building2, ChevronDown, Filter, Heart, Info, MapPin, Sparkles, UserCircle, Zap } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// Example recommended jobs data
const recommendedJobs = [
  {
    id: 1,
    title: "Frontend Developer",
    company: "TechCorp Solutions",
    location: "Remote",
    matchPercentage: 95,
    salary: "$90k - $120k",
    skills: ["React", "TypeScript", "CSS"],
    reasonForMatch: ["Based on your React experience", "Matches your remote preference"],
    applications: 24,
    postedDays: 2,
  },
  {
    id: 2,
    title: "Web Architect",
    company: "Digital Innovations",
    location: "San Francisco, CA",
    matchPercentage: 90,
    salary: "$130k - $160k",
    skills: ["Architecture", "Cloud", "JavaScript"],
    reasonForMatch: ["Similar to your previous applications", "Matches your skill level"],
    applications: 18,
    postedDays: 3,
  },
  {
    id: 3,
    title: "Full Stack Developer",
    company: "StartUp Inc",
    location: "New York, NY",
    matchPercentage: 88,
    salary: "$100k - $140k",
    skills: ["Node.js", "React", "PostgreSQL"],
    reasonForMatch: ["Matches your full stack experience", "Similar company size"],
    applications: 42,
    postedDays: 1,
  },
]

export default function RecommendationsScreen() {
  const router = useRouter()
  const [savedJobs, setSavedJobs] = useState<number[]>([])

  const toggleSaveJob = (jobId: number) => {
    setSavedJobs((prev) => (prev.includes(jobId) ? prev.filter((id) => id !== jobId) : [...prev, jobId]))
  }

  return (
    <TooltipProvider>
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
          <div className="space-y-6">
            {/* Header Section */}
            <div className="flex items-end justify-between">
              <div className="space-y-1">
                <h1 className="text-2xl font-semibold tracking-tight">For You</h1>
                <p className="flex items-center space-x-2 text-muted-foreground">
                  <Sparkles className="h-4 w-4" />
                  <span>Recommendations based on your application history</span>
                </p>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm" className="space-x-2">
                    <Filter className="h-4 w-4" />
                    <span>Filter</span>
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-[200px]">
                  <DropdownMenuItem>Highest Match</DropdownMenuItem>
                  <DropdownMenuItem>Most Recent</DropdownMenuItem>
                  <DropdownMenuItem>Salary Range</DropdownMenuItem>
                  <DropdownMenuItem>Location</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            {/* Recommendations Grid */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {recommendedJobs.map((job) => (
                <Card key={job.id} className="flex flex-col justify-between p-6">
                  {/* Job Header */}
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div className="space-y-1">
                        <h2 className="font-semibold hover:text-primary">
                          <Button
                            variant="link"
                            className="h-auto p-0 text-left text-base font-semibold"
                            onClick={() => router.push(`/jobs/${job.id}`)}
                          >
                            {job.title}
                          </Button>
                        </h2>
                        <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                          <Building2 className="h-4 w-4" />
                          <span>{job.company}</span>
                        </div>
                      </div>
                      <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => toggleSaveJob(job.id)}>
                        <Heart
                          className={`h-5 w-5 ${
                            savedJobs.includes(job.id) ? "fill-primary text-primary" : "text-muted-foreground"
                          }`}
                        />
                      </Button>
                    </div>

                    {/* Match Percentage */}
                    <div className="flex items-center space-x-2">
                      <div className="flex h-8 items-center space-x-2 rounded-full bg-primary/10 px-3 text-sm font-medium text-primary">
                        <Zap className="h-4 w-4" />
                        <span>{job.matchPercentage}% Match</span>
                      </div>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Button variant="ghost" size="icon" className="h-8 w-8">
                            <Info className="h-4 w-4" />
                          </Button>
                        </TooltipTrigger>
                        <TooltipContent>
                          <div className="space-y-2">
                            <p className="font-medium">Why this match?</p>
                            <ul className="list-inside list-disc text-sm">
                              {job.reasonForMatch.map((reason, index) => (
                                <li key={index}>{reason}</li>
                              ))}
                            </ul>
                          </div>
                        </TooltipContent>
                      </Tooltip>
                    </div>

                    {/* Job Details */}
                    <div className="space-y-2 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-2">
                        <MapPin className="h-4 w-4" />
                        <span>{job.location}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span>{job.salary}</span>
                      </div>
                    </div>

                    {/* Skills */}
                    <div className="flex flex-wrap gap-2">
                      {job.skills.map((skill) => (
                        <span key={skill} className="rounded-full bg-secondary px-3 py-1 text-xs">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Job Footer */}
                  <div className="mt-4 flex items-center justify-between border-t pt-4 text-sm text-muted-foreground">
                    <span>{job.applications} applications</span>
                    <span>Posted {job.postedDays} days ago</span>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </main>
      </div>
    </TooltipProvider>
  )
}

