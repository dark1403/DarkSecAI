<template>
  <div class="space-y-8">
    <!-- Page Header -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-900/20 via-blue-900/20 to-cyan-900/20 p-8 border border-purple-500/20 backdrop-blur-sm">
      <div class="absolute inset-0 bg-grid-white/5"></div>
      <div class="relative z-10">
        <div class="flex items-center gap-3 mb-2">
          <div class="p-3 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-xl">
            <UIcon name="i-heroicons-users" class="h-8 w-8 text-purple-400" />
          </div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Developer Showcase
          </h1>
        </div>
        <p class="text-gray-300 text-lg">Meet the talented developers behind DarkSec-AI</p>
      </div>
    </div>

    <!-- Developers Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <UCard
        v-for="developer in developers"
        :key="developer.id"
        class="group bg-gradient-to-br from-gray-800/80 to-gray-900/80 backdrop-blur-sm border border-gray-700/50 shadow-xl hover:shadow-2xl hover:shadow-purple-500/20 transition-all duration-300 hover:scale-[1.02] overflow-hidden"
      >
        <!-- Developer Image -->
        <div class="relative overflow-hidden">
          <img
            :src="developer.image"
            :alt="developer.name"
            class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>

          <!-- Status Badge -->
          <!-- <div class="absolute top-4 right-4">
            <UBadge
              :color="developer.status === 'Available' ? 'green' : developer.status === 'Busy' ? 'yellow' : 'gray'"
              variant="solid"
              size="sm"
            >
              <UIcon :name="developer.statusIcon" class="h-3 w-3 mr-1" />
              {{ developer.status }}
            </UBadge>
          </div> -->
        </div>

        <!-- ⬇️ Use the DEFAULT slot instead of #body -->
        <div class="p-6 space-y-4">
          <!-- Name and Role -->
          <div>
            <h3 class="text-xl font-bold text-white mb-1">{{ developer.name }}</h3>
            <p class="text-purple-400 font-medium">{{ developer.role }}</p>
          </div>

          <!-- Bio -->
          <p class="text-gray-300 text-sm leading-relaxed">{{ developer.bio }}</p>

          <!-- Skills -->
          <div>
            <h4 class="text-sm font-semibold text-gray-400 mb-2">Expertise</h4>
            <div class="flex flex-wrap gap-2">
              <UBadge
                v-for="skill in developer.skills"
                :key="skill"
                variant="soft"
                color="purple"
                size="xs"
              >
                {{ skill }}
              </UBadge>
            </div>
          </div>

          <!-- Stats -->
          <!-- <div class="grid grid-cols-3 gap-4 pt-2 border-t border-gray-700/50">
            <div class="text-center">
              <div class="text-lg font-bold text-white">{{ developer.projects }}</div>
              <div class="text-xs text-gray-400">Projects</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-white">{{ developer.experience }}</div>
              <div class="text-xs text-gray-400">Years Exp</div>
            </div>
            <div class="text-center">
              <div class="text-lg font-bold text-white">{{ developer.contributions }}</div>
              <div class="text-xs text-gray-400">Commits</div>
            </div>
          </div> -->

          <!-- Social Links -->
          <!-- <div class="flex gap-3 pt-2">
            <UButton
              v-for="link in developer.socialLinks"
              :key="link.platform"
              :to="link.url"
              :icon="link.icon"
              size="sm"
              variant="ghost"
              color="purple"
              target="_blank"
              rel="noopener noreferrer"
              class="hover:bg-purple-500/20"
            >
              {{ link.platform }}
            </UButton>
          </div> -->
        </div>
      </UCard>
    </div>

    <!-- Call to Action -->
    <!-- <UCard class="bg-gradient-to-br from-purple-900/20 to-blue-900/20 border border-purple-500/20 backdrop-blur-sm">
      <div class="text-center py-8">
        <div class="inline-block p-4 bg-gradient-to-br from-purple-500/20 to-blue-500/20 rounded-full mb-6">
          <UIcon name="i-heroicons-heart" class="h-12 w-12 text-purple-400" />
        </div>
        <h3 class="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-3">
          Join Our Team
        </h3>
        <p class="text-gray-300 mb-6 max-w-2xl mx-auto">
          Are you passionate about cybersecurity and AI? We're always looking for talented developers to join our mission of making the web safer.
        </p>
        <div class="flex gap-4 justify-center">
          <UButton
            to="/contact"
            icon="i-heroicons-envelope"
            color="purple"
            size="lg"
            class="shadow-xl shadow-purple-500/25 hover:shadow-2xl hover:shadow-purple-500/40 transition-all hover:scale-105"
          >
            Get in Touch
          </UButton>
          <UButton
            to="/careers"
            icon="i-heroicons-briefcase"
            variant="outline"
            size="lg"
            class="border-2 hover:bg-white/5 transition-all hover:scale-105"
          >
            View Openings
          </UButton>
        </div>
      </div>
    </UCard> -->
  </div>
</template>

<script setup>
definePageMeta({
  middleware: ['auth']
});

// Developer data
const developers = ref([
  {
    id: 1,
    name: "Prathmesh Singhan-Patil",
    role: "Lead Security Engineer",
    image: "/developers/img-1.jpeg",
    bio: "Lead security engineer with hands-on expertise in ethical hacking, cloud infrastructure, and enterprise security architecture. Skilled in threat modeling, incident response, and securing large-scale distributed systems. Passionate about mentoring teams and driving forward AI-driven cybersecurity solutions.",
    skills: [
      "Certified Ethical Hacker",
      "Certified Azure Administrator",
      "Penetration Testing",
      "Cloud Security",
      "Incident Response",
      "Security Architecture"
    ],
    status: "Available",
    statusIcon: "i-heroicons-check-circle",
    // projects: 24,
    // experience: 8,
    // contributions: 1247,
    // socialLinks: [
    //   {
    //     platform: "GitHub",
    //     icon: "i-simple-icons-github",
    //     url: "https://github.com/alexchen"
    //   },
    //   {
    //     platform: "LinkedIn",
    //     icon: "i-simple-icons-linkedin",
    //     url: "https://linkedin.com/in/alexchen"
    //   },
    //   {
    //     platform: "Twitter",
    //     icon: "i-simple-icons-twitter",
    //     url: "https://twitter.com/alexchen"
    //   }
    // ]
  },
  {
    id: 2,
    name: "Mohd kaif A R Solkar",
    role: "Cybersecurity Enthusiasts",
    image: "/developers/img-2.jpeg",
    bio: "Aspiring cybersecurity specialist passionate about ethical hacking and secure coding practices. Currently focusing on building expertise in network defense, malware analysis, and threat intelligence.",
    skills: ["Ethical Hacking", "Networking", "Linux", "Python", "Threat Analysis"],
    status: "Busy",
    statusIcon: "i-heroicons-clock",
    // projects: 18,
    // experience: 6,
    // contributions: 892,
    // socialLinks: [
    //   {
    //     platform: "GitHub",
    //     icon: "i-simple-icons-github",
    //     url: "https://github.com/sarahrodriguez"
    //   },
    //   {
    //     platform: "LinkedIn",
    //     icon: "i-simple-icons-linkedin",
    //     url: "https://linkedin.com/in/sarahrodriguez"
    //   },
    //   {
    //     platform: "Portfolio",
    //     icon: "i-heroicons-globe-alt",
    //     url: "https://sarahrodriguez.dev"
    //   }
    // ]
  },
  {
    id: 3,
    name: "Areeb shakil Modak",
    role: "Cyberseurity Enthusiasts",
    image: "/developers/img-3.jpeg",
    bio: "Enthusiastic learner exploring the fields of penetration testing, vulnerability assessment, and secure web development. Actively contributing to open-source security tools and capture-the-flag (CTF) competitions.",
    skills: ["Penetration Testing", "Web Security", "C++", "Python", "CTFs"],
    status: "Available",
    statusIcon: "i-heroicons-check-circle",
    // projects: 16,
    // experience: 7,
    // contributions: 1156,
    // socialLinks: [
    //   {
    //     platform: "GitHub",
    //     icon: "i-simple-icons-github",
    //     url: "https://github.com/marcusjohnson"
    //   },
    //   {
    //     platform: "LinkedIn",
    //     icon: "i-simple-icons-linkedin",
    //     url: "https://linkedin.com/in/marcusjohnson"
    //   },
    //   {
    //     platform: "Kaggle",
    //     icon: "i-simple-icons-kaggle",
    //     url: "https://kaggle.com/marcusjohnson"
    //   }
    // ]
  },
  {
    id: 4,
    name: "Nischay Naik",
    role: "Web Designer",
    image: "/developers/img-4.jpeg",
    bio: "Creative web designer with a passion for crafting visually appealing and user-friendly interfaces. Experienced in responsive design, UI/UX principles, and integrating modern front-end technologies with strong cybersecurity awareness.",
    skills: ["HTML", "CSS", "JavaScript", "Figma", "UI/UX Design", "Responsive Design"],
    status: "Away",
    statusIcon: "i-heroicons-x-circle",
    // projects: 21,
    // experience: 5,
    // contributions: 743,
    // socialLinks: [
    //   {
    //     platform: "GitHub",
    //     icon: "i-simple-icons-github",
    //     url: "https://github.com/emilyzhang"
    //   },
    //   {
    //     platform: "LinkedIn",
    //     icon: "i-simple-icons-linkedin",
    //     url: "https://linkedin.com/in/emilyzhang"
    //   },
    //   {
    //     platform: "Medium",
    //     icon: "i-simple-icons-medium",
    //     url: "https://medium.com/@emilyzhang"
    //   }
    // ]
  }
]);
</script>
