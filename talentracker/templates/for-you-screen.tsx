"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import {
  Heart,
  Search,
  UserCircle,
  Building2,
  MapPin,
  Clock,
  ChevronDown,
  Code2,
  Briefcase,
  GraduationCap,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"

// Example job data
const jobs = [
  {
    id: 1,
    title: "Senior Web Developer",
    company: "TechCorp Solutions",
    location: "San Francisco, CA",
    type: "Full-time",
    posted: "2 days ago",
    skills: ["React", "Node.js", "TypeScript"],
    salary: "$120k - $150k",
    level: "Senior",
  },
  {
    id: 2,
    title: "Frontend Developer",
    company: "Digital Innovations",
    location: "Remote",
    type: "Full-time",
    posted: "1 day ago",
    skills: ["Vue.js", "CSS", "JavaScript"],
    salary: "$90k - $110k",
    level: "Mid-Level",
  },
  {
    id: 3,
    title: "Full Stack Engineer",
    company: "StartUp Inc",
    location: "New York, NY",
    type: "Full-time",
    posted: "3 days ago",
    skills: ["Python", "React", "PostgreSQL"],
    salary: "$100k - $130k",
    level: "Mid-Senior",
  },
  {
    id: 4,
    title: "Backend Developer",
    company: "Enterprise Solutions",
    location: "Chicago, IL",
    type: "Contract",
    posted: "5 days ago",
    skills: ["Java", "Spring", "MySQL"],
    salary: "$115k - $140k",
    level: "Senior",
  },
]

export default function ForYouScreen() {
  const router = useRouter()
  const [savedJobs, setSavedJobs] = useState<number[]>([])

  const toggleSaveJob = (jobId: number) => {
    setSavedJobs((prev) => (prev.includes(jobId) ? prev.filter((id) => id !== jobId) : [...prev, jobId]))
  }

  return (
    <div className="min-h-screen w-full bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary">
              <span className="text-lg font-bold text-primary-foreground">TT</span>
            </div>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="space-x-2">
                  <span>Discover</span>
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="start" className="w-[200px]">
                <DropdownMenuItem>
                  <Code2 className="mr-2 h-4 w-4" /> Development
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <Briefcase className="mr-2 h-4 w-4" /> Business
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <GraduationCap className="mr-2 h-4 w-4" /> Education
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          <div className="flex items-center space-x-4">
            <div className="hidden md:block">
              <div className="relative">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input type="search" placeholder="Search jobs..." className="w-[300px] pl-8" />
              </div>
            </div>
            <UserCircle className="h-8 w-8" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-6">
        <div className="space-y-6">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">For You</h1>
            <p className="text-muted-foreground">Jobs matching your interests and experience</p>
          </div>

          {/* Job Cards Grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {jobs.map((job) => (
              <Card key={job.id} className="flex flex-col justify-between p-6 hover:shadow-lg transition-shadow">
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
                      <span className="sr-only">Save job</span>
                    </Button>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                      <MapPin className="h-4 w-4" />
                      <span>{job.location}</span>
                    </div>
                    <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                      <Clock className="h-4 w-4" />
                      <span>{job.posted}</span>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {job.skills.map((skill) => (
                      <span
                        key={skill}
                        className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="mt-6 flex items-center justify-between">
                  <span className="text-sm font-medium">{job.salary}</span>
                  <span className="text-sm text-muted-foreground">{job.level}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}

