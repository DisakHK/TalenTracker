"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { ArrowUpDown, Building2, Clock, Heart, MapPin, SearchIcon, Sparkles, UserCircle, X, Zap } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"

// Example search results
const searchResults = [
  {
    id: 1,
    title: "Website Developer (Fixed Term)",
    company: "Tech Solutions Ltd",
    location: "Remote",
    salary: "$80k - $100k",
    type: "Contract (6 months)",
    requirements: ["React", "Node.js", "TypeScript"],
    posted: "2 days ago",
    matchScore: 95,
  },
  {
    id: 2,
    title: "Frontend Developer (Contract)",
    company: "Digital Agency Inc",
    location: "New York, NY",
    salary: "$90k - $110k",
    type: "Contract (12 months)",
    requirements: ["Vue.js", "JavaScript", "CSS"],
    posted: "1 day ago",
    matchScore: 88,
  },
  {
    id: 3,
    title: "Web Application Developer",
    company: "StartUp Co",
    location: "San Francisco, CA",
    salary: "$95k - $120k",
    type: "Full-time",
    requirements: ["Angular", "TypeScript", "AWS"],
    posted: "3 days ago",
    matchScore: 82,
  },
]

// Example related recommendations
const recommendations = [
  {
    id: 4,
    title: "Full Stack Developer",
    company: "Tech Innovators",
    location: "Remote",
    salary: "$100k - $130k",
    type: "Full-time",
    requirements: ["React", "Python", "PostgreSQL"],
    posted: "1 day ago",
    matchScore: 85,
  },
  {
    id: 5,
    title: "JavaScript Developer",
    company: "Web Solutions",
    location: "Chicago, IL",
    salary: "$85k - $105k",
    type: "Full-time",
    requirements: ["JavaScript", "React", "Node.js"],
    posted: "4 days ago",
    matchScore: 80,
  },
]

export default function SearchResultsScreen() {
  const router = useRouter()
  const [savedJobs, setSavedJobs] = useState<number[]>([])
  const [activeFilters] = useState(["Remote", "Contract", "Full-time"])

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
          </div>
          <UserCircle className="h-8 w-8" />
        </div>
      </header>

      {/* Main Content */}
      <main className="container py-6">
        <div className="space-y-6">
          {/* Search Summary */}
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <h1 className="text-2xl font-semibold tracking-tight">Website Development Jobs</h1>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <SearchIcon className="h-4 w-4" />
                <span>24 results found</span>
              </div>
            </div>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="space-x-2">
                  <ArrowUpDown className="h-4 w-4" />
                  <span>Sort</span>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem>Most Relevant</DropdownMenuItem>
                <DropdownMenuItem>Newest First</DropdownMenuItem>
                <DropdownMenuItem>Highest Salary</DropdownMenuItem>
                <DropdownMenuItem>Best Match</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* Active Filters */}
          <div className="flex flex-wrap items-center gap-2">
            {activeFilters.map((filter) => (
              <Badge key={filter} variant="secondary">
                {filter}
                <Button variant="ghost" size="icon" className="ml-1 h-4 w-4 p-0 hover:bg-transparent">
                  <X className="h-3 w-3" />
                </Button>
              </Badge>
            ))}
            <Button variant="ghost" size="sm" className="text-muted-foreground">
              Clear all
            </Button>
          </div>

          {/* Search Results */}
          <div className="space-y-4">
            {searchResults.map((job) => (
              <Card key={job.id} className="p-6">
                <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center space-x-2">
                        <h2 className="text-xl font-semibold">{job.title}</h2>
                        <Badge variant="secondary" className="space-x-1">
                          <Zap className="h-3 w-3" />
                          <span>{job.matchScore}% Match</span>
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-2 text-muted-foreground">
                        <Building2 className="h-4 w-4" />
                        <span>{job.company}</span>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-2">
                        <MapPin className="h-4 w-4" />
                        <span>{job.location}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Clock className="h-4 w-4" />
                        <span>{job.type}</span>
                      </div>
                      <div>{job.salary}</div>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {job.requirements.map((req) => (
                        <Badge key={req} variant="outline">
                          {req}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <div className="flex flex-row gap-2 md:flex-col">
                    <Button className="flex-1 md:w-32" onClick={() => router.push(`/jobs/${job.id}/apply`)}>
                      Quick Apply
                    </Button>
                    <Button variant="outline" size="icon" className="md:w-32" onClick={() => toggleSaveJob(job.id)}>
                      <Heart className={`h-4 w-4 ${savedJobs.includes(job.id) ? "fill-primary text-primary" : ""}`} />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          {/* Related Recommendations */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <h2 className="text-xl font-semibold">Recommendations based on your search</h2>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              {recommendations.map((job) => (
                <Card key={job.id} className="p-6">
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold">{job.title}</h3>
                        <Button variant="ghost" size="icon" onClick={() => toggleSaveJob(job.id)}>
                          <Heart
                            className={`h-4 w-4 ${savedJobs.includes(job.id) ? "fill-primary text-primary" : ""}`}
                          />
                        </Button>
                      </div>
                      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                        <Building2 className="h-4 w-4" />
                        <span>{job.company}</span>
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-2">
                        <MapPin className="h-4 w-4" />
                        <span>{job.location}</span>
                      </div>
                      <div>{job.salary}</div>
                    </div>

                    <div className="flex flex-wrap gap-2">
                      {job.requirements.map((req) => (
                        <Badge key={req} variant="outline">
                          {req}
                        </Badge>
                      ))}
                    </div>

                    <Button className="w-full" variant="outline" onClick={() => router.push(`/jobs/${job.id}`)}>
                      View Details
                    </Button>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

