"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import {
  Building2,
  Clock,
  Globe2,
  Heart,
  Home,
  MapPin,
  SearchIcon,
  Settings2,
  UserCircle,
  Users2,
  X,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"

// Example suggested jobs
const suggestedJobs = [
  {
    id: 1,
    title: "Senior Frontend Developer",
    company: "TechCorp Solutions",
    location: "Remote",
    salary: "$100k - $130k",
    type: "Full-time",
    posted: "2 days ago",
  },
  {
    id: 2,
    title: "UX/UI Designer",
    company: "Design Studio Inc",
    location: "New York, NY",
    salary: "$90k - $110k",
    type: "Full-time",
    posted: "1 day ago",
  },
  {
    id: 3,
    title: "Backend Engineer",
    company: "StartUp Co",
    location: "San Francisco, CA",
    salary: "$120k - $150k",
    type: "Contract",
    posted: "3 days ago",
  },
]

const filterOptions = [
  { id: "full-time", label: "Full-time", icon: Clock },
  { id: "remote", label: "Remote", icon: Home },
  { id: "office", label: "Office", icon: Building2 },
  { id: "hybrid", label: "Hybrid", icon: Users2 },
  { id: "worldwide", label: "Worldwide", icon: Globe2 },
]

export default function SearchScreen() {
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState("")
  const [activeFilters, setActiveFilters] = useState<string[]>([])
  const [savedJobs, setSavedJobs] = useState<number[]>([])

  const toggleFilter = (filterId: string) => {
    setActiveFilters((prev) => (prev.includes(filterId) ? prev.filter((id) => id !== filterId) : [...prev, filterId]))
  }

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
          {/* Search Section */}
          <div className="space-y-4">
            <h1 className="text-2xl font-semibold tracking-tight">Search Jobs</h1>
            <div className="relative">
              <SearchIcon className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
              <Input
                className="pl-9"
                placeholder="Search by title, company, or keywords..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              {searchQuery && (
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute right-2 top-2"
                  onClick={() => setSearchQuery("")}
                >
                  <X className="h-4 w-4" />
                </Button>
              )}
            </div>
          </div>

          {/* Quick Filters */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="font-medium">Quick Filters</h2>
              <Button
                variant="ghost"
                size="sm"
                className="text-sm text-muted-foreground"
                onClick={() => setActiveFilters([])}
              >
                Clear all
              </Button>
            </div>
            <div className="flex flex-wrap gap-2">
              {filterOptions.map((filter) => {
                const Icon = filter.icon
                return (
                  <Button
                    key={filter.id}
                    variant={activeFilters.includes(filter.id) ? "default" : "outline"}
                    className="space-x-2"
                    onClick={() => toggleFilter(filter.id)}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{filter.label}</span>
                  </Button>
                )
              })}
            </div>
          </div>

          {/* Suggested Jobs */}
          <div className="space-y-4">
            <h2 className="font-medium">You May Be Interested In</h2>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {suggestedJobs.map((job) => (
                <Card key={job.id} className="flex flex-col justify-between p-6">
                  <div className="space-y-4">
                    <div className="flex items-start justify-between">
                      <div className="space-y-1">
                        <h3 className="font-semibold hover:text-primary">
                          <Button
                            variant="link"
                            className="h-auto p-0 text-left text-base font-semibold"
                            onClick={() => router.push(`/jobs/${job.id}`)}
                          >
                            {job.title}
                          </Button>
                        </h3>
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
                    <div className="space-y-2 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-2">
                        <MapPin className="h-4 w-4" />
                        <span>{job.location}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Clock className="h-4 w-4" />
                        <span>{job.type}</span>
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center justify-between border-t pt-4">
                    <span className="text-sm font-medium">{job.salary}</span>
                    <span className="text-sm text-muted-foreground">{job.posted}</span>
                  </div>
                </Card>
              ))}
            </div>
          </div>

          {/* Advanced Search */}
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" className="w-full space-x-2">
                <Settings2 className="h-4 w-4" />
                <span>Advanced Search</span>
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Advanced Search Options</DialogTitle>
              </DialogHeader>
              <div className="space-y-6 py-4">
                {/* Experience Level */}
                <div className="space-y-4">
                  <Label>Experience Level</Label>
                  <RadioGroup defaultValue="any">
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="any" id="any" />
                      <Label htmlFor="any">Any</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="entry" id="entry" />
                      <Label htmlFor="entry">Entry Level</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="mid" id="mid" />
                      <Label htmlFor="mid">Mid Level</Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="senior" id="senior" />
                      <Label htmlFor="senior">Senior Level</Label>
                    </div>
                  </RadioGroup>
                </div>

                {/* Salary Range */}
                <div className="space-y-4">
                  <Label>Salary Range</Label>
                  <Slider defaultValue={[50000, 150000]} max={200000} min={0} step={5000} />
                  <div className="flex justify-between text-sm text-muted-foreground">
                    <span>$0</span>
                    <span>$200k+</span>
                  </div>
                </div>

                {/* Additional Options */}
                <div className="space-y-4">
                  <Label>Additional Options</Label>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="visa" className="text-sm">
                        Visa Sponsorship
                      </Label>
                      <Switch id="visa" />
                    </div>
                    <div className="flex items-center justify-between">
                      <Label htmlFor="recent" className="text-sm">
                        Posted in last 24h
                      </Label>
                      <Switch id="recent" />
                    </div>
                  </div>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </main>
    </div>
  )
}

